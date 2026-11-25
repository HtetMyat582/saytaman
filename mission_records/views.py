from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from .models import MissionRecord, MissionRecordPhoto
from .forms import MissionRecordForm, MissionFuelRefillFormSet
from vehicles.models import Vehicle
from django.utils import timezone
from django.utils.text import get_valid_filename
from pathlib import Path
import requests
from members.access import has_dashboard_access


def save_mission_photos(mission, uploads):
	mission_number = get_valid_filename(
		str(mission.mission_number).replace('/', '-')
	)

	for upload in uploads:
		extension = Path(upload.name).suffix.lower()
		number = mission.mission_photos.count() + 1
		filename = f'{mission_number}-{number:02d}{extension}'
		storage_path = f'mission_photos/{filename}'

		while default_storage.exists(storage_path):
			number += 1
			filename = f'{mission_number}-{number:02d}{extension}'
			storage_path = f'mission_photos/{filename}'

		upload.name = filename
		MissionRecordPhoto.objects.create(mission=mission, image=upload)



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
		form = MissionRecordForm(request.POST, request.FILES)
		fuel_formset = MissionFuelRefillFormSet(
			request.POST,
			request.FILES,
			prefix='fuel_refills',
		)

		is_form_valid = form.is_valid()
		is_fuel_formset_valid = fuel_formset.is_valid()

		if is_form_valid and is_fuel_formset_valid:
			form.instance.created_by = member
			mission = form.save()

			save_mission_photos(mission, form.cleaned_data['photos'])

			vehicle = mission.vehicle
			vehicle.mission_status = 'On Mission'
			fuel_formset.instance = mission
			fuel_formset.save()
			vehicle.save()

			messages.success(request, 'Mission record saved.')
			return redirect('mission_list')
		messages.error(request, 'Please correct the errors below.')
	else:
		form = MissionRecordForm()
		fuel_formset = MissionFuelRefillFormSet(prefix='fuel_refills')

	return render(request, 'mission_records/add_mission.html', {
		'form': form,
		'can_edit_mission_number': False,
		'fuel_formset': fuel_formset,
		'now': now,
	})

def mission_details(request, pk):
	mission = get_object_or_404(
		MissionRecord.objects.prefetch_related('fuel_refills'),
		pk=pk,
	)
	photos = mission.mission_photos.all()
	form = MissionRecordForm(instance=mission)
	now = timezone.now().year
	
	driver_trimmed = mission.driver_name.member_id[-3:]
	assist_1_trimmed = mission.assistant_1.member_id[-3:]
	if mission.assistant_2:
		assist_2_trimmed = mission.assistant_2.member_id[-3:]
	else:
		assist_2_trimmed = None
	
	member = getattr(request.user, 'member_profile', None)
	is_fb_admin = has_dashboard_access(member) if request.user.is_authenticated else False
	
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
	can_edit_mission_number = bool(member and member.role == 'Admin')

	# Permission: driver or assistant_1 or assistant_2 can edit
	allowed = False

	if member and (
		mission.driver_name == member
		or (mission.assistant_1 and mission.assistant_1 == member)
		or (mission.assistant_2 and mission.assistant_2 == member)
		or member.role == 'Admin'
		or has_dashboard_access(member)
	):
		allowed = True

	if not allowed:
		messages.error(request, 'You do not have permission to edit this mission.')
		return redirect('mission_list')

	if request.method == 'POST':
		current_vehicle = mission.vehicle
		photos_to_delete = mission.mission_photos.filter(
			pk__in=request.POST.getlist('delete_photos')
		)
		remaining_photo_count = (
			mission.mission_photos.count() - photos_to_delete.count()
		)

		form = MissionRecordForm(
			request.POST,
			request.FILES,
			instance=mission,
			can_edit_mission_number=can_edit_mission_number,
		)
		form.fields['photos'].max_files = max(
			0, 10 - remaining_photo_count
		)

		fuel_formset = MissionFuelRefillFormSet(
			request.POST,
			request.FILES,
			instance=mission,
			prefix='fuel_refills',
		)

		is_form_valid = form.is_valid()
		is_fuel_formset_valid = fuel_formset.is_valid()

		if is_form_valid and is_fuel_formset_valid:
			if mission.vehicle != current_vehicle and not mission.back_to_hq:
				messages.error(
					request,
					'Cannot change the vehicle for an active mission. '
					'Mark it as returned first.',
				)
				form.fields['vehicle'].initial = current_vehicle.pk
			else:
				mission = form.save()
				photos_to_delete.delete()
				save_mission_photos(mission, form.cleaned_data['photos'])
				fuel_formset.save()

				messages.success(request, 'Mission record updated.')
				return redirect('mission_details', pk)

		messages.error(request, 'Please correct the errors below.')
	else:
		form = MissionRecordForm(
			instance=mission,
			can_edit_mission_number=can_edit_mission_number,
		)
		form.fields['photos'].max_files = max(
			0, 10 - mission.mission_photos.count()
		)
		fuel_formset = MissionFuelRefillFormSet(
			instance=mission,
			prefix='fuel_refills',
		)

	return render(request, 'mission_records/edit_mission.html', {
		'form': form,
		'fuel_formset': fuel_formset,
		'mission': mission,
		'can_edit_mission_number': can_edit_mission_number,
		'now': now,
	})


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
		upload_url = f"https://graph.facebook.com/v24.0/{settings.PAGE_ID}/photos"

		for photo_record in photos:
			if not photo_record.image:
				continue

			try:
				with open(photo_record.image.path, 'rb') as image_file:
					files = {
						'source': (photo_record.image.name, image_file, 'image/jpeg')
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
			'access_token': settings.PAGE_ACCESS_TOKEN,
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