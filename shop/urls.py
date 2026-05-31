from django.urls import path
from . import views
urlpatterns = [
    path('acheter/<int:product_id>/', views.acheter, name='acheter'),
]