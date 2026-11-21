from django.urls import path

from . import views

urlpatterns = [
    path('', views.fuel_refill_list, name='fuel_refill_list'),
    path('add/', views.fuel_refill_add, name='fuel_refill_add'),
    path('<int:pk>/edit/', views.fuel_refill_edit, name='fuel_refill_edit'),
    path('<int:pk>/delete/', views.fuel_refill_delete, name='fuel_refill_delete'),
]