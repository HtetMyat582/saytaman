from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('toggle-locale/', views.toggle_language, name='set_language'),
    path('profile/', views.profile, name='profile'),
    path('members/', include('members.urls')),
    path('', include('web_portal.auth_urls')),
]
