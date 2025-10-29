from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberProfileForm, UserEmailForm


@login_required
def profile(request):
    user = request.user
    member = getattr(user, 'member_profile', None)
    if not member:
        messages.error(request, "No member profile linked to your account.")
        return redirect('home')

    if request.method == 'POST':
        mform = MemberProfileForm(request.POST, request.FILES, instance=member)
        uform = UserEmailForm(request.POST, instance=user)
        if mform.is_valid() and uform.is_valid():
            uform.save()
            mform.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('member_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        mform = MemberProfileForm(instance=member)
        uform = UserEmailForm(instance=user)

    readonly = {
        'member_id': member.member_id,
        'name': member.name,
        'role': member.role,
        'nrc': member.nrc,
        'dob': member.dob,
        'blood_type': member.blood_type,
        'father_name': member.father_name,
        'mother_name': member.mother_name,
        'registration_date': member.registration_date,
    }

    return render(request, 'members/profile/profile.html', {
        'mform': mform,
        'uform': uform,
        'readonly': readonly,
        'member': member,
    })
