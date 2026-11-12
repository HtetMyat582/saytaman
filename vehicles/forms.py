from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id',
                  'license_plate',
                  'license_expirary_date',
                  'color',
                  'model',
                  'status',
                  'mission_status',
                  'photo']

        widgets = {
            'vehicle_id': forms.TextInput(attrs={'class': 'form-input'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-input'}),
            'license_expirary_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input'}),
            'model': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'mission_status': forms.Select(attrs={'class': 'form-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

