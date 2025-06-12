from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('toggle-locale/', views.toggle_language, name='set_language'),
]