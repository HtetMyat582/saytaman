from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import DashboardAccess


def has_dashboard_access(member):
    if member is None or not member.is_active:
        return False

    return DashboardAccess.objects.filter(
        member=member,
        member__is_active=True,
        is_active=True,
    ).exists()


def dashboard_access_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        member = getattr(request.user, 'member_profile', None)
        if not has_dashboard_access(member):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped