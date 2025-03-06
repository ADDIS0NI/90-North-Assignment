from django.urls import path
from . import views

urlpatterns = [
    path('', views.drive_home, name='drive_home'),
    path('connect/', views.connect_drive, name='connect_drive'),
    path('upload/', views.upload_file, name='upload_file'),
    path('list/', views.file_list, name='file_list'),
    path('download/<str:file_id>/', views.download_file, name='download_file'),
]