from django.urls import path

from . import views

urlpatterns = [
    path('', views.fuel_refill_list, name='fuel_refill_list'),
    path('add/', views.fuel_refill_add, name='fuel_refill_add'),
]