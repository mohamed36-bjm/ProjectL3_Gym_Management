# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # غير home_view بالاسم الصحيح لدالتك
]