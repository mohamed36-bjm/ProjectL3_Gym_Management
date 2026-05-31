from django.urls import path
from . import views

urlpatterns = [
    path("statistiques/", views.manager_statistiques, name="manager_statistiques"),
    path("dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("send-notification/", views.send_notification, name="send_notification"),
     path('user-info/<int:user_id>/', views.user_info, name='user_info'),
     path('manage-shop/', views.manage_shop, name='manage_shop'),
]