from django.urls import path
from . import views

urlpatterns = [
    path('', views.athlete_profile_view, name='athlete_profile_view'),
    path('creer-seance/', views.creer_seance, name='creer_seance'),
    path('reserver-seance/<int:seance_id>/', views.booking, name='reserver_seance'),
    path('supprimer-seance/<int:seance_id>/', views.supprimer_seance, name='supprimer_seance'),
    path('update-profile/', views.update_profile, name='update_profile'),
path('delete-notification/<int:notif_id>/', views.delete_notification, name='delete_notification'),
]