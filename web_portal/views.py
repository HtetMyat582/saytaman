from django.shortcuts import render
from django.utils.translation import gettext as _
from datetime import datetime
from django.http import HttpResponseRedirect
from django.utils.translation import activate, check_for_language
from django.conf import settings

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
