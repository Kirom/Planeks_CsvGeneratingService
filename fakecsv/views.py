from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django_celery_results.models import TaskResult

from fakecsv.forms import DataSchemaForm, ColumnFormSet, DataSetForm
from fakecsv.models import DataSchema, DataSet

from .tasks import generate_csv_task


@login_required
def generate_csv(request, pk=None):
    """Generate csv via ajax."""
    if request.method == 'POST':
        rows = int(request.POST.get('rows'))
        response_data = {}
        data_schema = DataSchema.objects.filter(id=pk).first()
        new_data_set = DataSet.objects.create(created=timezone.now(),
                                              status='Processing',
                                              data_schema=data_schema)
        task = generate_csv_task.delay(rows, data_schema.name, new_data_set.id)
        response_data['result'] = 'Successful'
        response_data['task_id'] = task.task_id
        response_data['csv_file_id'] = new_data_set.id
        created = new_data_set.created
        response_data['created'] = created
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'result': 'Failed! =('}, status=400)


def check_task_status(request, task_id):
    """Helper function for ajax."""
    task_result = TaskResult.objects.filter(task_id=task_id)[0].result
    data = {'result': task_result}
    return JsonResponse(data)


@login_required
def download_csv(request, pk=None, id=None):
    """Download result csv file."""
    data_schema = DataSchema.objects.filter(id=pk).first()
    csv_file = f'{data_schema}_{id}.csv'
    response = FileResponse(default_storage.open(csv_file, 'rb'))
    return response


class DataSchemasListView(LoginRequiredMixin, ListView):
    """Data schema list."""
    login_url = '/accounts/login'
    queryset = DataSchema.objects.all()
    template_name = 'fakecsv/home.html'


class DataSchemaDeleteView(SuccessMessageMixin,
                           LoginRequiredMixin,
                           DeleteView):
    """Data schema delete view."""
    login_url = '/accounts/login'
    model = DataSchema
    template_name = 'fakecsv/delete.html'
    success_url = reverse_lazy('fakecsv:data_schema_list')
    success_message = 'Data schema deleted successfully!'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DataSchemaDeleteView, self).delete(
            request, *args, **kwargs)


class DataSchemaCreateView(SuccessMessageMixin,
                           LoginRequiredMixin,
                           CreateView):
    """Data schema create view."""
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


class DataSchemaUpdateView(SuccessMessageMixin,
                           LoginRequiredMixin,
                           UpdateView):
    """Data schema update view."""
    model = DataSchema
    login_url = '/accounts/login'
    form_class = DataSchemaForm
    template_name = 'fakecsv/create.html'
    success_url = reverse_lazy('fakecsv:data_schema_list')
    success_message = 'Data schema updated successfully!'

    def get_context_data(self, **kwargs):
        data = super(DataSchemaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = ColumnFormSet(self.request.POST,
                                            instance=self.object)
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


@login_required
def data_sets_view(request, pk=None):
    """Data sets list of specific data schema."""
    form = DataSetForm()
    object_list = DataSet.objects.select_related().filter(data_schema=pk)
    data_schema = DataSchema.objects.select_related().filter(id=pk).first()
    return render(request, 'fakecsv/data_sets_list.html',
                  context={'object_list': object_list,
                           'data_schema': data_schema,
                           'form': form})
