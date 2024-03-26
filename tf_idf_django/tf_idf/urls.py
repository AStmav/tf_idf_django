from django.urls import path
from .views import upload_file, result_view

urlpatterns = [
    path('upload_form/', upload_file, name='upload_file'),
    path('result/', result_view, name='result_view'),
]
