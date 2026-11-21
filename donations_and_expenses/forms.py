from django import forms
from django.utils.translation import gettext_lazy as _
from .models import FuelRefill


class FuelRefillForm(forms.ModelForm):
    class Meta:
        model = FuelRefill
        fields = ('vehicle', 'date', 'time', 'pump_name', 'liters', 'fuel_type', 'cost', 'notes', 'fuel_voucher_photo')
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'pump_name': forms.TextInput(attrs={'class': 'form-input'}),
            'liters': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0.01', 'step': '0.01',
            }),
            'fuel_type': forms.Select(attrs={'class': 'form-input'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0', 'step': '1',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3,
            }),
            'fuel_voucher_photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'vehicle': _('Vehicle'),
            'date': _('Date'),
            'time': _('Time'),
            'pump_name': _('Pump Name'),
            'liters': _('Liters'),
            'fuel_type': _('Fuel Type'),
            'cost': _('Cost'),
            'notes': _('Notes'),
            'fuel_voucher_photo': _('Fuel Voucher Photo'),
        }  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = self.fields['vehicle'].queryset.order_by('vehicle_id')