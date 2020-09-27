import csv
import random
from random import choice
from string import ascii_uppercase, ascii_lowercase


def _generate_full_name():
    name = ''.join(choice(ascii_uppercase)) + ''.join(
        choice(ascii_lowercase) for i in range(random.randint(3, 8)))
    surname = ''.join(choice(ascii_uppercase)) + ''.join(
        choice(ascii_lowercase) for i in range(random.randint(3, 12)))
    return f'{name} {surname}'


def _generate_company_name():
    company_name = ''
    for i in range(random.randint(1, 4)):
        random_word = ''.join(choice(ascii_uppercase)) + ''.join(
            choice(ascii_lowercase) for i in range(random.randint(3, 15)))
        company_name += f'{random_word} '
    company_name += 'Inc.'
    return company_name


def _generate_date():
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    date = f'20{random.randint(10, 20)}-' \
           f'{str(month) if month >= 10 else "0" + str(month)}-' \
           f'{str(day) if day >= 10 else "0" + str(day)}'
    return date


JOBS_LIST = ['Psychologist', 'Budget analyst', 'Occupational Therapist',
             'Actor', 'Speech-Language Pathologist', 'Surveyor',
             'Firefighter,', 'School Psychologist', 'Carpenter',
             'Statistician', 'Mechanical Engineer', 'Event Planner',
             'Medical Assistant', 'Landscape Architect', 'Judge',
             'School Counselor', 'Janitor', 'IT Manager', 'Hairdresser',
             'Computer Systems Administrator', 'Financial Advisor',
             'Educator', 'Mason', 'Massage Therapist',
             'Middle School Teacher', 'Logistician', 'Executive Assistant',
             'Security Guard', 'Recreation & Fitness Worker',
             'Photographer', 'Fitness Trainer', 'Insurance Agent',
             'Diagnostic Medical Sonographer', 'Landscaper & Groundskeeper',
             'Chemist', 'Electrical Engineer', 'Patrol Officer',
             'Physical Therapist', 'Anthropologist', 'Farmer',
             'Physicist', 'Police Officer', 'Radiologic Technologist',
             'Truck Driver', 'Human Resources Assistant', 'Receptionist',
             'Elementary School Teacher', 'Actuary',
             'Systems Analyst', 'Cost Estimator']

EMAIL_DOMAINS_LIST = ['gmail.com', 'yahoo.com', 'hotmail.com', 'msn.com',
                      'aol.com', 'yahoo.fr']


class CsvWriter:
    """Csv writer class."""

    def __init__(self, file_name, columns, rows):
        """Initialize writer's instance."""
        self.fieldnames = []
        self.file_name = file_name
        self.columns = columns
        self.rows = rows

    def get_init_vals(self, file):
        """Initialize fieldnames, separator, quote"""
        for column in self.columns:
            self.fieldnames.insert(column.order, column.name)
            separator = column.data_schema.column_separator
            quote = column.data_schema.string_character
        self.writer = csv.DictWriter(file,
                                     fieldnames=self.fieldnames,
                                     delimiter=separator,
                                     quotechar=quote)
        self.writer.writeheader()

    def write_rows(self):
        """Write rows into csv file"""
        for i in range(self.rows):
            row = {}
            for column in self.columns:
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
                    job = choice(JOBS_LIST)
                    row[column.name] = job
                elif column.data_type == 'EMAIL':
                    email = ''.join(
                        choice(ascii_lowercase) for i in range(random.randint(3, 12))) + '@' + choice(
                        EMAIL_DOMAINS_LIST)
                    row[column.name] = email
                elif column.data_type == 'DATE':
                    date = _generate_date()
                    row[column.name] = date

            self.writer.writerow(row)

    def run(self):
        with open(self.file_name, 'w') as csv_file:
            self.get_init_vals(csv_file)
            self.write_rows()

