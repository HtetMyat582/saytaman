from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.urls import reverse_lazy

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
]
