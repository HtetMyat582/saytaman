from django.shortcuts import render
from django.utils.translation import gettext as _
from datetime import datetime

def home(request):
    title = _("SayTaMan Social Welfare Association")
    now = datetime.now().year
    return render(request, 'index.html', {'title': title, 'now': now})
