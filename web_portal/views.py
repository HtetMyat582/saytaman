from django.shortcuts import render
from django.utils.translation import gettext as _
from datetime import datetime
from django.http import HttpResponseRedirect
from django.utils.translation import activate, check_for_language
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from members.models import Member

def home(request):
    user = request.user
    member = getattr(user, 'member_profile', None)
    title = _("Saytaman Social Welfare Association")
    now = datetime.now().year

    if not member:
        return render(request, 'index.html',
                      {
                          'title': title,
                          'now': now,
                       })
    else:
        return render(request, 'index.html',
                      {
                          'member_role': member.role,
                          'title': title,
                          'now': now,
                       })


def toggle_language(request):
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    current = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
    next_lang = 'my' if current == 'en' else 'en'
    response = HttpResponseRedirect(next_url)
    if check_for_language(next_lang):
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, next_lang)
        activate(next_lang)
    return response

"""
@login_required
def profile(request):
    Render a simple user profile page for the authenticated user.
    title = _("Profile")
    now = datetime.now().year
    user = request.user
    member = getattr(user, 'member_profile', None)
    return render(request, 'profile.html',
                  {
                      'title': title,
                      'user': user,
                      'member_role': member.role,
                      'now': now
                      })

"""
class MemberPasswordChangeView(auth_views.PasswordChangeView):
    """Subclass PasswordChangeView to clear the member.must_change_password flag after a successful change."""
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        member = getattr(user, 'member_profile', None)
        if member:
            member.must_change_password = False
            member.save(update_fields=['must_change_password'])
        return response

@login_required
def member_list(request):
    members = Member.objects.order_by('-member_id')[:]
    now = datetime.now().year
    
    return render(request, 'members/member_list.html',{'members': members, 'now': now})