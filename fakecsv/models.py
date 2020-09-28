from django.db import models
from django.utils import timezone


class DataSchema(models.Model):
    """Data schemas model."""
    name = models.CharField(max_length=100, verbose_name='Name')
    column_separator = models.CharField(max_length=100,
                                        choices=[(',', 'Comma (,)'),
                                                 (';', 'Semicolon (;)')],
                                        verbose_name='Column separator')
    string_character = models.CharField(max_length=100,
                                        choices=[('"', 'Double qoute (")'),
                                                 ("'", "Single quote (')")],
                                        verbose_name='String character')
    modified = models.DateField(blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        """Define meta data."""
        verbose_name = 'Data schema'
        verbose_name_plural = 'Data schemas'
        ordering = ['name']


class Column(models.Model):
    """Columns model."""

    class DataTypes(models.TextChoices):
        FULL_NAME = 'FN', 'Full name'
        JOB = 'JOB', 'Job'
        EMAIL = 'EMAIL', 'Email'
        COMPANY_NAME = 'CN', 'Company name'
        INTEGER = 'INT', 'Integer'
        DATE = 'DATE', 'Date'

    name = models.CharField(max_length=100, verbose_name='Name')
    data_schema = models.ForeignKey(DataSchema, related_name='has_columns',
                                    on_delete=models.CASCADE)
    range_from = models.PositiveIntegerField(blank=True, null=True)
    range_to = models.PositiveIntegerField(blank=True, null=True)
    order = models.PositiveIntegerField()
    data_type = models.CharField(max_length=10, choices=DataTypes.choices)

    def __str__(self):
        """String representation of model."""
        return f'[{self.data_schema}] {self.name}'

    class Meta:
        """Define meta data."""
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'
        ordering = ['data_schema']


class DataSet(models.Model):
    """Data sets model."""
    created = models.DateField(blank=True, default=timezone.now)
    status = models.CharField(max_length=10, default='Processing')
    data_schema = models.ForeignKey(DataSchema, related_name='has_data_sets',
                                    on_delete=models.CASCADE)

    def __str__(self):
        """String representation of model."""
        return f'[{self.data_schema}] {self.created}'

    class Meta:
        """Define meta data."""
        verbose_name = 'Data set'
        verbose_name_plural = 'Data sets'
        ordering = ['data_schema']
