from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  
    path('login/', views.login_view, name='login'),
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('logout/', views.logout_view, name='logout'),
]