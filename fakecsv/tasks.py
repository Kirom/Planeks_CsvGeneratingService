"""Tasks for celery."""
from django.utils import timezone

import os

from Planeks_CsvGeneratingService.celery import app
from Planeks_CsvGeneratingService.settings import MEDIA_ROOT

from .models import DataSchema, DataSet, Column

from .services.csv_generator import CsvWriter


@app.task(bind=True)
def generate_csv_task(self, rows, pk):
    """Generate csv in background via celery."""
    data_schema = DataSchema.objects.filter(id=pk).first()
    new_data_set = DataSet.objects.create(created=timezone.now(),
                                          status='Processing',
                                          data_schema=data_schema)
    csv_file = os.path.join(MEDIA_ROOT, f'{data_schema}_{new_data_set.id}.csv')
    columns = Column.objects.select_related().filter(
        data_schema__name=data_schema)
    csv_writer = CsvWriter(csv_file, columns, rows)
    csv_writer.run()
    DataSet.objects.filter(id=new_data_set.id).update(status='Ready')
    return 'Ready'
