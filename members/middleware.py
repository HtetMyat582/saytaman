from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    """Redirect users that have `member_profile.must_change_password` set to True
    to the password change page until they update their password.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for anonymous users and staff/superuser
        if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
            member = getattr(request.user, 'member_profile', None)
            if member and member.must_change_password:
                # allow access only to the password change views and logout
                path = request.path_info
                allowed = [
                    reverse('password_change'),
                    reverse('password_change_done'),
                    reverse('logout'),
                ]
                if not any(path.startswith(a) for a in allowed):
                    return redirect('password_change')
        return self.get_response(request)
