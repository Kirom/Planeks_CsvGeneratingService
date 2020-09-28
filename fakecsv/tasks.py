"""Tasks for celery."""
import csv
import os
import random
from string import ascii_lowercase

from celery.result import AsyncResult
from django.utils import timezone

from Planeks_CsvGeneratingService.celery import app
from .models import DataSchema, DataSet, Column
from .services.csv_generator import CsvWriter, _generate_full_name, _generate_company_name, JOBS_LIST, \
    EMAIL_DOMAINS_LIST, _generate_date
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
    # csv_writer = CsvWriter(csv_file, columns, rows)
    # csv_writer.run()
    fieldnames = []
    for column in columns:
        fieldnames.insert(column.order, column.name)
        separator = column.data_schema.column_separator
        quote = column.data_schema.string_character
    with open(csv_file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=fieldnames,
                                delimiter=separator,
                                quotechar=quote)
        writer.writeheader()
        for i in range(rows):
            row = {}
            for column in columns:
                if column.data_type == 'FN':
                    full_name = _generate_full_name()
                    row[column.name] = full_name
                elif column.data_type == 'INT':
                    result_integer = random.randint(column.range_from, column.range_to)
                    row[column.name] = result_integer
                elif column.data_type == 'CN':
                    company_name = _generate_company_name()
                    row[column.name] = company_name
                elif column.data_type == 'JOB':
                    job = random.choice(JOBS_LIST)
                    row[column.name] = job
                elif column.data_type == 'EMAIL':
                    email = ''.join(
                        random.choice(ascii_lowercase) for i in range(random.randint(3, 12))) + '@' + choice(
                        EMAIL_DOMAINS_LIST)
                    row[column.name] = email
                elif column.data_type == 'DATE':
                    date = _generate_date()
                    row[column.name] = date

            writer.writerow(row)

    DataSet.objects.filter(id=new_data_set.id).update(status='Ready')
    return 'Ready'
