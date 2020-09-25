from django.contrib import admin

from fakecsv.models import Column, DataSchema, DataSet


@admin.register(DataSchema)
class DataSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'column_separator', 'string_character', ]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'data_type', 'order', 'data_schema__name']

    def data_schema__name(self, obj):
        return obj.data_schema.name


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ['created', 'status', 'data_schema__name']

    def data_schema__name(self, obj):
        return obj.data_schema.name
