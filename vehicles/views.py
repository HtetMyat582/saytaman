from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from vehicles.models import Vehicle
from mission_records.models import MissionRecord

@login_required
def vehicle_list(request):

    member = getattr(request.user, 'member_profile', None)
    if not member:
        messages.error(request, 'Only members can view vehicle list.')
        return redirect('home')

    vehicles_o_mission = Vehicle.objects.order_by('mission_status')
    vehicles_o_id = Vehicle.objects.all()

    now = timezone.now().year
    context = {'vehicles_o_mission': vehicles_o_mission,
               'vehicles_o_id': vehicles_o_id,
               'now': now}

    return render(request, 'vehicles/vehicle_list.html', context)

@login_required
def vehicle_details(request, pk):
    now = timezone.now().year
    vehicle = get_object_or_404(Vehicle, pk=pk)
    missions_count = MissionRecord.objects.filter(Q(vehicle=vehicle)).count()

    try:
        current_mission = MissionRecord.objects.filter(Q(vehicle=vehicle) & Q(back_to_hq=None)).get()

        context = {
            'vehicle': vehicle,
            'current_mission': current_mission,
            'missions_count': missions_count,
            'now': now
            }
        return render(request, 'vehicles/vehicle_details.html', context)

    except MissionRecord.DoesNotExist:
        context = {
            'vehicle': vehicle,
            'missions_count': missions_count,
            'now': now
            }
        return render(request, 'vehicles/vehicle_details.html', context)