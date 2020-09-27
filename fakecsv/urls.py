from django.urls import path

from fakecsv.views import DataSchemasListView, \
    DataSchemaDeleteView, DataSchemaCreateView, DataSchemaUpdateView, data_sets_view, generate_csv, download_csv, \
    check_task_status

urlpatterns = [
    path('', DataSchemasListView.as_view(), name='data_schema_list'),
    path('<int:pk>/data_sets/generate_csv/', generate_csv, name='generate_csv'),
    path('<int:pk>/data_sets/download_csv/<int:id>/', download_csv, name='download_csv'),
    path('delete/<int:pk>/', DataSchemaDeleteView.as_view(), name='delete_data_schema'),
    path('create/', DataSchemaCreateView.as_view(), name='create'),
    path('update/<int:pk>/', DataSchemaUpdateView.as_view(), name='update_data_schema'),
    path('<int:pk>/data_sets/', data_sets_view, name='data_sets_list'),
    path('check_task_status/<str:task_id>/', check_task_status, name='check_task_status'),
]
