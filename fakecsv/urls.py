from django.urls import path

from fakecsv.views import DataSchemasListView, \
    DataSchemaDeleteView, DataSchemaCreateView, DataSchemaUpdateView, data_sets_view, generate_csv, download_csv

urlpatterns = [
    path('', DataSchemasListView.as_view(), name='data_schema_list'),
    # path('export_csv/<int:pk>/', export_csv, name='export_csv'),
    # path('generate_csv/<str:data_schema>/', generate_csv, name='generate_csv'),
    path('<int:pk>/data_sets/generate_csv/', generate_csv, name='generate_csv'),
    path('<int:pk>/data_sets/download_csv/<int:id>/', download_csv, name='download_csv'),
    path('delete/<int:pk>/', DataSchemaDeleteView.as_view(), name='delete_data_schema'),
    path('create/', DataSchemaCreateView.as_view(), name='create'),
    path('update/<int:pk>/', DataSchemaUpdateView.as_view(), name='update_data_schema'),
    path('<int:pk>/data_sets/', data_sets_view, name='data_sets_list'),
]
