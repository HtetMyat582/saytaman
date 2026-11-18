from django import forms
from django.utils.translation import gettext_lazy as _
from .models import FuelRefill


class FuelRefillForm(forms.ModelForm):
    class Meta:
        model = FuelRefill
        fields = ('vehicle', 'date', 'time', 'pump_name', 'liters', 'cost', 'notes')
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'pump_name': forms.TextInput(attrs={'class': 'form-control'}),
            'liters': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0.01', 'step': '0.01',
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0', 'step': '1',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
            }),
        }
        labels = {
            'vehicle': _('Vehicle'),
            'date': _('Date'),
            'time': _('Time'),
            'pump_name': _('Pump Name'),
            'liters': _('Liters'),
            'cost': _('Cost'),
            'notes': _('Notes'),
        }  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = self.fields['vehicle'].queryset.order_by('vehicle_id')