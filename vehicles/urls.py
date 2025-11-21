from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_details, name='vehicle_details'),
]
