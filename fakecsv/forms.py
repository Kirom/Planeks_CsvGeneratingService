from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, \
    Fieldset, Div, HTML, ButtonHolder, Submit

from django import forms
from django.forms import inlineformset_factory

from fakecsv.models import DataSchema, Column
from fakecsv.services.custom_layout_object import Formset


class ColumnForm(forms.ModelForm):
    """Form for data schema column."""

    class Meta:
        """Define meta data."""
        model = Column
        exclude = ()


ColumnFormSet = inlineformset_factory(
    DataSchema, Column, form=ColumnForm,
    fields=['name', 'data_type', 'range_from', 'range_to', 'order'],
    extra=1,
    can_delete=True
)


class DataSchemaForm(forms.ModelForm):
    """Form for Data schema model."""

    class Meta:
        """Define meta data."""
        model = DataSchema
        exclude = ()

    def __init__(self, *args, **kwargs):
        """Initialize form."""
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
                ButtonHolder(Submit('submit', 'Submit')),
            )
        )


class DataSetForm(forms.Form):
    """Form for data set model."""
    rows = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        """Initialize form."""
        super(DataSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Field('rows'),
            ButtonHolder(Submit('submit', 'Generate data',
                                css_class='btn btn-success')),
        )
        self.helper.form_action = 'generate_csv/'
