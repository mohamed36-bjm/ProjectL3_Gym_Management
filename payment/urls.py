from django.urls import path
from . import views
from compteprofile.views import athlete_profile_view
from login.views import login_view
urlpatterns = [
    path('payer/',views.payer,name='payer'),
    path('acheter/<int:product_id>/', views.payer_achat, name='payer_achat'),
    path('profile/', athlete_profile_view, name='athlete_profile_view'),
    path('login/', login_view, name='login_view'),
    path('ReservationDetailes/<int:seance_id>/', views.ReservationDetailes, name='reservation_details'),
    path('CancelReservation/<int:seance_id>/', views.CancelReservation, name='cancel_res'),
]