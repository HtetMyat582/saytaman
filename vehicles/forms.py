from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id',
                  'license_plate',
                  'license_expiry_date',
                  'color',
                  'model',
                  'status',
                  'mission_status',
                  'photo']

        widgets = {
            'vehicle_id': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'STM-1',
            }),
            'license_plate': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'License plate',
            }),
            'license_expiry_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-input',
                'placeholder': 'License expiry date',
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Vehicle color',
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Vehicle model',
            }),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'mission_status': forms.Select(attrs={'class': 'form-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

