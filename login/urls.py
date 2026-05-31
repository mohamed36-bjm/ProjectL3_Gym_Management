from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('manager-login/', views.manager_login, name='manager_login'),
]