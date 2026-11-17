from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.translation import activate, check_for_language
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from members.models import Member
from mission_records.models import MissionRecord
from natural_disasters.models import DisasterEvent, DisasterEventPhoto
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.db.models import Sum

from donations_and_expenses.models import Donation, Expense, FuelRefill
from members.access import dashboard_access_required
from vehicles.models import Vehicle

def weekly_food_counter():
    # Sunday, Dec 14, 2025, 3:00 PM)
    start_date = datetime(2025, 12, 14, 18, 0, 0)
    now = datetime.now()
    
    if now < start_date:
        return 0
    
    diff = now - start_date
    weeks_passed = diff.days // 7
    
    return 172 + weeks_passed

def home(request):
    user = request.user
    member = getattr(user, 'member_profile', None)
    title = _("Saytaman Social Welfare Association")
    now = timezone.now().year
    missions = MissionRecord.objects.all().order_by('-date', '-time')
    missions_count = missions.count()
    weekly_food_count = weekly_food_counter()

    if not member:
        return render(request, 'index.html',
                      {
                          'title': title,
                          'now': now,
                          'missions_count': missions_count,
                          'weekly_food_count': weekly_food_count,
                       })
    else:
        return render(request, 'index.html',
                      {
                          'member_role': member.role,
                          'missions': missions,
                          'missions_count': missions_count,
                          'weekly_food_count': weekly_food_count,
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
    now = timezone.now().year
    
    return render(request, 'members/member_list.html',{'members': members, 'now': now})

def our_missions(request):
    now = timezone.now().year
    title = _("Our Mission")
    missions = MissionRecord.objects.all().order_by('-date', '-time')
    missions_count = missions.count()
    weekly_food_count = weekly_food_counter()

    context = {
        'now': now,
        'title': title,
        'missions_count': missions_count,
        'weekly_food_count': weekly_food_count,
        }
    return render(request, 'web_portal/our_missions.html', context)

def disaster_response(request):
    now = timezone.now().year
    title = _("Disaster Response")
    disaster_events = DisasterEvent.objects.all().order_by('-date')
    #event = get_object_or_404(DisasterEvent, pk=pk)
    #event_photos = event.disaster_photos.all()
    context = {
        'now': now,
        'title': title,
        'disaster_events': disaster_events,
        #'event': event,
        #'event_photos': event_photos
        }
    return render(request, 'web_portal/disaster_response.html', context)

@dashboard_access_required
def management_dashboard(request):
    today = timezone.localdate()
    period = request.GET.get('period', 'month')

    if period == 'week':
        start_date = today - timedelta(days=today.weekday())
    elif period == 'year':
        start_date = date(today.year, 1, 1)
    else:
        period = 'month'
        start_date = date(today.year, today.month, 1)

    period_missions = MissionRecord.objects.filter(
        date__range=(start_date, today)
    )
    mission_totals = period_missions.aggregate(
        donations=Sum('donation_received'),
        expenses=Sum('mission_expenses'),
        fuel=Sum('fuel_cost'),
    )

    donation_total = (
        Donation.objects.filter(date__range=(start_date, today))
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )
    expense_total = (
        Expense.objects.filter(date__range=(start_date, today))
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    refill_period = FuelRefill.objects.filter(
        date__range=(start_date, today)
    )
    off_mission_fuel_total = (
        refill_period.aggregate(total=Sum('cost'))['total']
        or Decimal('0')
    )
    recent_refills = refill_period.select_related(
        'vehicle', 'created_by'
    ).order_by('-date', '-time')[:10]

    # The latest mission without a return-to-HQ time is shown as active.
    active_missions = (
        MissionRecord.objects
        .filter(back_to_hq__isnull=True)
        .select_related('vehicle', 'driver_name')
        .order_by('-date', '-time')
    )
    active_by_vehicle = {}
    for mission in active_missions:
        active_by_vehicle.setdefault(mission.vehicle_id, mission)

    vehicles = list(Vehicle.objects.order_by('vehicle_id'))
    for vehicle in vehicles:
        vehicle.active_mission = active_by_vehicle.get(vehicle.pk)
        if vehicle.active_mission:
            vehicle.dashboard_status = 'On Mission'
        elif vehicle.status in ('Inactive', 'Service'):
            vehicle.dashboard_status = 'Unavailable'
        else:
            vehicle.dashboard_status = 'Stand-by'

    return render(request, 'management/dashboard.html', {
        'now': today.year,
        'period': period,
        'start_date': start_date,
        'end_date': today,
        'vehicles': vehicles,
        'mission_count': period_missions.count(),
        'donation_total': donation_total,
        'expense_total': expense_total,
        'mission_donations': mission_totals['donations'] or 0,
        'mission_expenses': mission_totals['expenses'] or 0,
        'mission_fuel': mission_totals['fuel'] or 0,
        'off_mission_fuel_total': off_mission_fuel_total,
        'recent_refills': recent_refills,
    })