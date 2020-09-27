import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django_celery_results.models import TaskResult

from fakecsv.services.csv_generator import CsvWriter
from fakecsv.tasks import generate_csv_task
from Planeks_CsvGeneratingService.settings import BASE_DIR, MEDIA_ROOT, S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY
from fakecsv.forms import DataSchemaForm, ColumnFormSet, DataSetForm
from fakecsv.models import DataSchema, DataSet, Column

import os
from django.http import JsonResponse


# Неоконченный вариант с JS
# def generate_csv(request, pk=None):
#     if request.method == 'POST':
#         form = DataSetForm(request.POST or None)
#         if form.is_valid():
#             data = form.cleaned_data
#             rows = data['rows']
#     else:
#         messages.error(request, message='Please input rows quantity')
#         form = DataSetForm()
#     task = generate_csv_task.delay(rows, pk)
#     data = {'task_id': task.task_id, }
#     response = JsonResponse(data)
#     return redirect('fakecsv:data_sets_list', pk=pk,)


# Рабочий вариант базовый без js
def generate_csv(request, pk=None):
    if request.method == 'POST':
        form = DataSetForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            rows = data['rows']
    else:
        messages.error(request, message='Please input rows quantity')
        form = DataSetForm()
    # data_schema = DataSchema.objects.filter(id=pk).first()
    # new_data_set = DataSet.objects.create(created=timezone.now(),
    #                                       status='Processing',
    #                                       data_schema=data_schema)
    # csv_file = os.path.join(MEDIA_ROOT, f'{data_schema}_{new_data_set.id}.csv')
    # columns = Column.objects.select_related().filter(data_schema__name=data_schema)
    # csv_writer = CsvWriter(csv_file, columns, rows)
    # csv_writer.run()
    # DataSet.objects.filter(id=new_data_set.id).update(status='Ready')
    generate_csv_task.delay(rows, pk)
    return redirect('fakecsv:data_sets_list', pk=pk)


# Helper function for ajax
def check_task_status(request, task_id):
    task_status = TaskResult.objects.filter(task_id=task_id)[0].status
    data = {'status': task_status}
    return JsonResponse(data)


def download_csv(request, pk=None, id=None):
    data_schema = DataSchema.objects.filter(id=pk).first()
    csv_file = os.path.join(MEDIA_ROOT, f'{data_schema}_{id}.csv')
    s3_client = boto3.client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             service_name='s3')
    downloaded_csv = f'{data_schema}_{id}.csv'
    s3_client.download_file(S3_BUCKET, csv_file, downloaded_csv)

    response = FileResponse(open(csv_file, 'rb'))
    return response


class DataSchemasListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login'
    queryset = DataSchema.objects.all()
    template_name = 'fakecsv/home.html'


class DataSchemaDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = DataSchema
    template_name = 'fakecsv/delete.html'
    success_url = reverse_lazy('fakecsv:data_schema_list')
    success_message = 'Data schema deleted successfully!'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DataSchemaDeleteView, self).delete(request, *args, **kwargs)


class DataSchemaCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = DataSchema
    login_url = '/accounts/login'
    form_class = DataSchemaForm
    template_name = 'fakecsv/create.html'
    success_url = reverse_lazy('fakecsv:data_schema_list')
    success_message = 'Data schema created successfully!'

    def get_context_data(self, **kwargs):
        data = super(DataSchemaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = ColumnFormSet(self.request.POST)
        else:
            data['columns'] = ColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.modified = timezone.now()
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(DataSchemaCreateView, self).form_valid(form)


class DataSchemaUpdateView(UpdateView):
    model = DataSchema
    login_url = '/accounts/login'
    form_class = DataSchemaForm
    template_name = 'fakecsv/create.html'
    success_url = reverse_lazy('fakecsv:data_schema_list')
    success_message = 'Data schema created successfully!'

    def get_context_data(self, **kwargs):
        data = super(DataSchemaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = ColumnFormSet(self.request.POST, instance=self.object)
        else:
            data['columns'] = ColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.modified = timezone.now()
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(DataSchemaUpdateView, self).form_valid(form)


def data_sets_view(request, pk=None):
    form = DataSetForm()
    object_list = DataSet.objects.select_related().filter(data_schema=pk)
    data_schema = DataSchema.objects.select_related().filter(id=pk).first()
    return render(request, 'fakecsv/data_sets_list.html',
                  context={'object_list': object_list,
                           'data_schema': data_schema,
                           'form': form})
