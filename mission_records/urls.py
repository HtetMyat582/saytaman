from django.urls import path
from . import views

urlpatterns = [
 path('', views.mission_list, name='mission_list'),
 path('add/', views.add_mission, name='add_mission'),
 path('edit/<int:pk>/', views.edit_mission, name='edit_mission'),
]
