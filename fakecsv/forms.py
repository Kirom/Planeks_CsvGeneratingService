from django import forms
from django.forms import inlineformset_factory

from fakecsv.models import DataSchema, Column

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from fakecsv.services.custom_layout_object import *


# class DataSchemaForm(forms.ModelForm):
#     # query_set = DataSchema.objects.all()
#     # column_separator_qs = DataSchema.objects.all().column_separator
#     # name = forms.CharField(label='Name',
#     #                        widget=forms.TextInput(
#     #                            attrs={'class': 'form-control form-control-sm'}))
#
#     # column_separator = forms.ChoiceField(label='Column separator',
#     #                                      widget=forms.Select(
#     #                                          attrs={'class': 'form-control js-example-basic-single'}))
#
#     # string_character = forms.ChoiceField(label='String character',
#     #                                      widget=forms.Select(
#     #                                          attrs={'class': 'form-control js-example-basic-single'}))
#
#     # travel_time = forms.CharField(label='Время в пути',
#     #                               widget=forms.NumberInput(
#     #                                   attrs={'class': 'form-control form-control-sm', 'placeholder': 'Часов'}))
#
#     class Meta:
#         model = DataSchema
#         fields = ('name', 'column_separator', 'string_character',)
#
#     def __init__(self, *args, **kwargs):
#         super(DataSchemaForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-sm'


# class ColumnForm(forms.ModelForm):
#     # query_set = DataSchema.objects.all()
#     # column_separator_qs = DataSchema.objects.all().column_separator
#     # name = forms.CharField(label='Name',
#     #                        widget=forms.TextInput(
#     #                            attrs={'class': 'form-control form-control-sm'}))
#     class Meta:
#         model = Column
#         fields = ('name', 'data_type', 'range_from', 'range_to', 'order')
#
#     def __init__(self, *args, **kwargs):
#         super(ColumnForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-sm'
class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        exclude = ()


ColumnFormSet = inlineformset_factory(
    DataSchema, Column, form=ColumnForm,
    fields=['name', 'data_type', 'range_from', 'range_to', 'order'], extra=1, can_delete=True
)


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(DataSchemaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('column_separator'),
                Field('string_character'),
                Fieldset('Schema columns',
                         Formset('columns')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
            )
        )


class DataSetForm(forms.Form):
    rows = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super(DataSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Field('rows'),
            ButtonHolder(Submit('submit', 'Generate data', css_class='btn btn-success')),
        )
        # self.helper.form_method = 'post'
        self.helper.form_action = 'generate_csv/'
