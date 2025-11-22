from django import forms
from django.contrib.auth import get_user_model
from .models import Member

User = get_user_model()


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['profile_photo', 'phone_number', 'address', 'husband_or_wife', 'job']
        widgets = {
            'address': forms.Select(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'husband_or_wife': forms.TextInput(attrs={'class': 'form-input'}),
            'job': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'husband_or_wife': 'Spouse',
            'profile_photo': 'Photo',
        }


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class MemberDetailsForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['profile_photo','member_id', 'name', 'role', 'nrc', 'dob', 'blood_type', 'is_active',
                  'address', 'phone_number', 'email',
                  'father_name', 'mother_name', 'husband_or_wife', 'job']

        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-input'}),
            'member_id': forms.TextInput(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'nrc': forms.TextInput(attrs={'class': 'form-input'}),
            'dob': forms.DateInput(attrs={'type':'date',' class': 'form-input'}),
            'blood_type': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'address': forms.Select(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'father_name': forms.TextInput(attrs={'class': 'form-input'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-input'}),
            'husband_or_wife': forms.TextInput(attrs={'class': 'form-input'}),
            'job': forms.TextInput(attrs={'class': 'form-input'}),
            }