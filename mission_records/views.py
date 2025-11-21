from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MissionRecord, MissionRecordPhoto
from .forms import MissionRecordForm, MissionRecordPhotoFormSet
from django.utils import timezone
import requests

fb_admin_id_list = ['STM-007', 'STM-014', 'STM-028', 'STM-144', 'STM-148', 'STM-172']


@login_required
def add_mission(request):
    """Allow any authenticated member to add a mission record.

    Members (driver or assistants) may create mission records while on mission.
    """
    now = timezone.now().year
    member = getattr(request.user, 'member_profile', None)
    if not member:
        messages.error(request, 'Only members can add mission records.')
        return redirect('home')

    

    if request.method == 'POST':
        form = MissionRecordForm(request.POST)
        formset = MissionRecordPhotoFormSet(request.POST, request.FILES)
        
        is_form_valid = form.is_valid()
        is_formset_valid = formset.is_valid()

        if is_form_valid and is_formset_valid:
            form.instance.created_by = member
            mission = form.save()
            vehicle = mission.vehicle
            vehicle.mission_status = 'On Mission'
            formset.instance = mission
            formset.save()
            vehicle.save()
            messages.success(request, 'Mission record saved.')
            return redirect('mission_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = MissionRecordForm()
        formset = MissionRecordPhotoFormSet(queryset=MissionRecordPhoto.objects.none())

    return render(request, 'mission_records/add_mission.html', {'form': form, 'formset': formset, 'now': now,})

def mission_details(request, pk):
    mission = get_object_or_404(MissionRecord, pk=pk)
    photos = mission.mission_photos.all()
    form = MissionRecordForm(instance=mission)
    now = timezone.now().year
    
    driver_trimmed = mission.driver_name.member_id[-3:]
    assist_1_trimmed = mission.assistant_1.member_id[-3:]
    assist_2_trimmed = mission.assistant_2.member_id[-3:]
    
    is_fb_admin = False
    if request.user.is_authenticated:
        member = getattr(request.user, 'member_profile', None)
        
        if member.member_id in fb_admin_id_list:
            is_fb_admin = True
    
    return render(request, 'mission_records/mission_details.html', {
        'mission': mission,
        'photos': photos,
        'form': form,
        'driver_name_trimmed': driver_trimmed,
        'assist_1_name_trimmed': assist_1_trimmed,
        'assist_2_name_trimmed': assist_2_trimmed,
        'now': now,
        'is_fb_admin': is_fb_admin,
        })


@login_required
def edit_mission(request, pk):
    """Allow editing by the driver or any assistant assigned to the mission."""
    mission = get_object_or_404(MissionRecord, pk=pk)
    member = getattr(request.user, 'member_profile', None)
    now = timezone.now().year

    # Permission: driver or assistant_1 or assistant_2 can edit
    allowed = False

    if member:
        if mission.driver_name == member or \
               (mission.assistant_1 and mission.assistant_1 == member) or \
               (mission.assistant_2 and mission.assistant_2 == member) or \
               member.role == 'Admin':
                allowed = True

    if not allowed:
        messages.error(request, 'You do not have permission to edit this mission.')
        return redirect('mission_list')

    if request.method == 'POST':
        current_vehicle = mission.vehicle

        form = MissionRecordForm(request.POST, instance=mission)
        formset = MissionRecordPhotoFormSet(request.POST, request.FILES, instance=mission)
        
        is_form_valid = form.is_valid()
        is_formset_valid = formset.is_valid()

        if is_form_valid and is_formset_valid:
            if mission.vehicle != current_vehicle and not mission.back_to_hq:
                messages.error(request, "Cannot change the vehicle for an active mission. Mark it as returned first.")
                form.fields['vehicle'].initial = current_vehicle.pk
            else:
                form.save()
                formset.save()
                messages.success(request, 'Mission record updated.')
            return redirect('mission_details', pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = MissionRecordForm(instance=mission)
        formset = MissionRecordPhotoFormSet(instance=mission)

    return render(request, 'mission_records/edit_mission.html', {'form': form, 'formset': formset,'mission': mission, 'now': now})


def mission_list(request):
    now = timezone.now().year
    missions = MissionRecord.objects.order_by('-date', '-time')[:50]
    return render(request, 'mission_records/mission_list.html', {'missions': missions, 'now': now})

@login_required
def post_to_facebook(request, pk):
    """Fetches a Django object, formats the text, and posts to Facebook."""
    try:
        mission = MissionRecord.objects.get(pk=pk)

    except MissionRecord.DoesNotExist:
        messages.error(request, 'Mission record not found.')
        return redirect('home') 

    photos = mission.mission_photos.all()

    message = f"""
🚨 စေတမန်လူမှုကူညီရေးအသင်းမှ
{mission.patient_type} အား (အခမဲ့)
သယ်ယူပို့ဆောင်ခြင်းမှတ်တမ်း 🚨

---
📍 လမ်းကြောင်းအမှတ်: {mission.mission_number}

* ရက်စွဲ: {mission.date}
* အချိန်: {mission.time}

👤 လူနာအချက်အလက်
* လူနာအမည်: {mission.patient_name}
* အသက်: {mission.patient_age} နှစ်

🗺️ ပို့ဆောင်မှု အသေးစိတ်
* စထွက်သည့်နေရာ: {mission.departure}
* ပို့​ဆောင်သည့်နေရာ: {mission.destination}

👷 စေတမန်အသင်းမှ
* ယာဥ်မောင်း: {mission.driver_name.name}
* အကူ: {mission.assistant_1.name}
* အကူ: {mission.assistant_2.name}

---
🚑 စေတမန်လူမှုကူညီရေးအသင်းမှ {mission.vehicle.vehicle_id} ယာဥ်ဖြင့် ကူညီပို့ဆောင်ပေးခဲ့ပါသည်။ 

📞 ဆက်သွယ်ရန်
၇၆လမ်း၊ ၃၇လမ်းနှင့် ၃၈လမ်းကြား၊ မန္တလေးမြို့
၀၉၄၃၁၀၀၇၈၆ / ၀၉၄၄၄၄၅၇၇၈၆

http://127.0.0.1:8000/missions/details/{mission.pk}

#စေတမန်လူမှုကူညီရေးအသင်း #လူမှုကူညီရေး #မန္တလေး
"""
    attachment_ids = []

    if photos.exists():
        upload_url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/photos"

        for photo_record in photos:
            if not photo_record.image:
                continue

            try:
                with open(photo_record.image.path, 'rb') as image_file:
                    files = {
                        'source': (photo_record.image.namem, image_file, 'image/jpeg')
                        }
                    data = {
                        'access_token': PAGE_ACCESS_TOKEN,
                        'published': False,
                        }

                    response = requests.post(upload_url, data=data, files=files)
                    response_data = response.json()

                    if response.status_code == 200 and 'id' in response_data:
                        attachment_ids.append(response_data['id'])
                    else:
                        print(f"Facebook Photo Upload Error for {photo_record.image.name}:", response_data)
        
            except FileNotFoundError:
                messages.warning(request, f"Warning: Photo file not found for {photo_record.image.name}. Skipping.")
            except Exception as e:
                print(f"General Upload Error for {photo_record.image.name}: {e}")

        if attachment_ids:
            post_url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/feed"

            post_data = {
                'message': message,
                'access_token': PAGE_ACCESS_TOKEN,
                }

            for photo_id in attachment_ids:
                post_data['attached_media[{}]'.format(len(post_data['attached_media']) if 'attached_media' in post_data else 0)] = '{"media_fbid": "%s"}' % photo_id

            response = request.post(post_url, data=post_data)
            response_data = response.json()

    
        else:
            post_url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/feed"
            data = {
                'message': message,
                'access_token': PAGE_ACCESS_TOKEN,
                'link': f"http://127.0.0.1:8000/missions/details/{mission.pk}"
            }
            response = requests.post(post_url, data=data)
            response_data = response.json()

    else:
        post_url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/feed"
        post_data = {
            'message': message,
            'access_token': PAGE_ACCESS_TOKEN,
            'link': f"http://127.0.0.1:8000/missions/details/{mission.pk}"
        }
        response = requests.post(post_url, data=post_data)
        response_data = response.json()

    if response.status_code == 200:
        messages.success(request, 'Successfully posted mission record to Facebook Page.')
        print("Successfully posted to Facebook:", response_data)
        return redirect('mission_details', pk=mission.pk)
    else:
        print("Facebook API Error:", response_data)
        messages.error(request, f'Facebook API Error: {response_data.get("error", {}).get("message", "Unknown error")}')
        return redirect('mission_details', pk=mission.pk)


@login_required
def set_back_to_hq(request, pk):
    if request.method == 'POST':
        mission = get_object_or_404(MissionRecord, pk=pk)
        
        member = getattr(request.user, 'member_profile', None)
        allowed = False
        if member:
            if mission.driver_name == member or \
               (mission.assistant_1 and mission.assistant_1 == member) or \
               (mission.assistant_2 and mission.assistant_2 == member) or \
               member.role == 'Admin':
                allowed = True

        if not allowed:
            messages.error(request, 'You do not have permission to mark this vehicle as returned.')
            return redirect('mission_details', pk=pk)

        
        if not mission.back_to_hq:
            mission.back_to_hq = timezone.now()
            mission.save()

            vehicle = mission.vehicle
            vehicle.mission_status = 'Stand-by'
            vehicle.save()
            
            messages.success(request, f"Vehicle {vehicle.vehicle_id} marked as returned and status set to Stand-by.")
        else:
            messages.warning(request, "Return time was already recorded.")

    return redirect('mission_details', pk=pk)