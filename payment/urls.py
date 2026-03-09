from django.urls import path
from . import views
from compteprofile.views import athlete_profile_view
from login.views import login_view
urlpatterns = [
    path('payer/',views.payer,name='payer'),
    path('profile/', athlete_profile_view, name='athlete_profile_view'),
    path('login/', login_view, name='login_view'),
]