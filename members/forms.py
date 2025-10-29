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
