from django.urls import path
from . import views
import web_portal.views as w_views

urlpatterns = [
    path('', w_views.member_list, name='member_list'),
    path('profile/', views.profile, name='member_profile'),
    path('edit/member/<int:pk>/', views.edit_member_details, name='member_details')
]
