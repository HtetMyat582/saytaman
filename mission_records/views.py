from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MissionRecord
from .forms import MissionRecordForm
from datetime import datetime

@login_required
def add_mission(request):
    """Allow any authenticated member to add a mission record.

    Members (driver or assistants) may create mission records while on mission.
    """
    now = datetime.now().year
    member = getattr(request.user, 'member_profile', None)
    if not member:
        messages.error(request, 'Only members can add mission records.')
        return redirect('home')

    if request.method == 'POST':
        form = MissionRecordForm(request.POST, request.FILES)
        if form.is_valid():
            mission = form.save()
            messages.success(request, 'Mission record saved.')
            return redirect('mission_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = MissionRecordForm()

    return render(request, 'mission_records/add_mission.html', {'form': form, 'now': now})

def mission_details(request, pk):
    mission = get_object_or_404(MissionRecord, pk=pk)
    form = MissionRecordForm(instance=mission)
    now = datetime.now().year
    driver_trimmed = str(mission.driver_name.member_id[-3:])
    assist_1_trimmed = str(mission.assistant_1.member_id[-3:])
    assist_2_trimmed = str(mission.assistant_2.member_id[-3:])

    return render(request, 'mission_records/mission_details.html', {
        'mission': mission,
        'form': form,
        'driver_name_trimmed': driver_trimmed,
        'assist_1_name_trimmed': assist_1_trimmed,
        'assist_2_name_trimmed': assist_2_trimmed,
        'now': now})


@login_required
def edit_mission(request, pk):
    """Allow editing by the driver or any assistant assigned to the mission."""
    mission = get_object_or_404(MissionRecord, pk=pk)
    member = getattr(request.user, 'member_profile', None)
    now = datetime.now().year
    # Permission: driver or assistant_1 or assistant_2 can edit
    allowed = False
    if member:
        if mission.driver_name == member:
            allowed = True
        if mission.assistant_1 and mission.assistant_1 == member:
            allowed = True
        if mission.assistant_2 and mission.assistant_2 == member:
            allowed = True
        if member.role == 'Admin':
            allowed = True

    if not allowed:
        messages.error(request, 'You do not have permission to edit this mission.')
        return redirect('mission_list')

    if request.method == 'POST':
        form = MissionRecordForm(request.POST, request.FILES, instance=mission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mission record updated.')
            return redirect('mission_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = MissionRecordForm(instance=mission)

    return render(request, 'mission_records/edit_mission.html', {'form': form, 'mission': mission, 'now': now})


def mission_list(request):
    now = datetime.now().year
    missions = MissionRecord.objects.order_by('-date', '-time')[:50]
    return render(request, 'mission_records/mission_list.html', {'missions': missions, 'now': now})
