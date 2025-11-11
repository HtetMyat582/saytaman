from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number',
                  'license_plate',
                  'license_expirary_date',
                  'color',
                  'model',
                  'status',
                  'mission_status',
                  'photo']
