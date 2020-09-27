"""Tasks for celery."""
import os

from celery.result import AsyncResult
from django.utils import timezone

from Planeks_CsvGeneratingService.celery import app
from .models import DataSchema, DataSet, Column
from .services.csv_generator import CsvWriter
from Planeks_CsvGeneratingService.settings import MEDIA_ROOT


@app.task(bind=True)
def generate_csv_task(self, rows, pk):
    """Generate csv in background via celery."""
    data_schema = DataSchema.objects.filter(id=pk).first()
    new_data_set = DataSet.objects.create(created=timezone.now(),
                                          status='Processing',
                                          data_schema=data_schema)
    csv_file = os.path.join(MEDIA_ROOT, f'{data_schema}_{new_data_set.id}.csv')
    columns = Column.objects.select_related().filter(data_schema__name=data_schema)
    csv_writer = CsvWriter(csv_file, columns, rows)
    csv_writer.run()
    DataSet.objects.filter(id=new_data_set.id).update(status='Ready')
    print(f'Проверка на существование файла {csv_file}:'
          f' {os.path.isfile(csv_file)} ')
    return 'Ready'
