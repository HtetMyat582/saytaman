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
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': '09 000 000 000',
            }),
            'husband_or_wife': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Spouse name',
            }),
            'job': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Occupation',
            }),
        }
        labels = {
            'husband_or_wife': 'Spouse',
            'profile_photo': 'Photo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].choices = [
            ('', 'Select township'),
            *Member.ADDRESS_CHOICES,
        ]


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'name@example.com',
            }),
        }


class MemberDetailsForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['profile_photo','member_id', 'name', 'role', 'nrc', 'dob', 'blood_type', 'is_active',
                  'address', 'phone_number', 'email',
                  'father_name', 'mother_name', 'husband_or_wife', 'job']

        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-input'}),
            'member_id': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'STM-000',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Full name',
            }),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'nrc': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'NRC number',
            }),
            'dob': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-input',
                'placeholder': 'Date of birth',
            }),
            'blood_type': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'address': forms.Select(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': '09 000 000 000',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input', 'placeholder': 'name@example.com',
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': "Father's name",
            }),
            'mother_name': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': "Mother's name",
            }),
            'husband_or_wife': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Spouse name',
            }),
            'job': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Occupation',
            }),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('', 'Select role'),
            *Member.ROLE_CHOICES,
        ]
        self.fields['blood_type'].choices = [
            ('', 'Select blood type'),
            *Member.BLOOD_TYPE_CHOICES,
        ]
        self.fields['address'].choices = [
            ('', 'Select township'),
            *Member.ADDRESS_CHOICES,
        ]
