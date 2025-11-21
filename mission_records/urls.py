from django.urls import path
from . import views

urlpatterns = [
    path('', views.mission_list, name='mission_list'),
    path('add/', views.add_mission, name='add_mission'),
    path('edit/<int:pk>/', views.edit_mission, name='edit_mission'),
    path('details/<int:pk>', views.mission_details, name='mission_details'),
    path('post-to-fb/<int:pk>/', views.post_to_facebook, name='post_to_facebook'),
    path('set-back-to-hq/<int:pk>', views.set_back_to_hq, name='set_back_to_hq'),
]
