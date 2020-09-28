"""Tasks for celery."""
from django.core.files.storage import default_storage
from django.utils import timezone

import os

from Planeks_CsvGeneratingService.celery import app
from Planeks_CsvGeneratingService.settings import MEDIA_ROOT

from .models import DataSchema, DataSet, Column

from .services.csv_generator import CsvWriter


@app.task(bind=True)
def generate_csv_task(self, rows, data_schema, new_data_set_id):
    """Generate csv in background via celery."""
    csv_file = f'{data_schema}_{new_data_set_id}.csv'
    columns = Column.objects.select_related().filter(
        data_schema__name=data_schema)
    csv_writer = CsvWriter(csv_file, columns, rows)
    csv_writer.run()
    DataSet.objects.filter(id=new_data_set_id).update(status='Ready')
    return 'Ready'
