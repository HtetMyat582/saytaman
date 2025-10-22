from django.shortcuts import render
from django.utils.translation import gettext as _
from datetime import datetime
from django.http import HttpResponseRedirect
from django.utils.translation import activate, check_for_language
from django.conf import settings
from django.contrib.auth.decorators import login_required

def home(request):
    title = _("Saytaman Social Welfare Association")
    now = datetime.now().year
    return render(request, 'index.html', {'title': title, 'now': now})


def toggle_language(request):
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    current = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
    next_lang = 'my' if current == 'en' else 'en'
    response = HttpResponseRedirect(next_url)
    if check_for_language(next_lang):
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, next_lang)
        activate(next_lang)
    return response


@login_required
def profile(request):
    """Render a simple user profile page for the authenticated user."""
    title = _("Profile")
    now = datetime.now().year
    user = request.user
    return render(request, 'profile.html', {'title': title, 'user': user, 'now': now})
