from django import forms
from django.forms import inlineformset_factory
from .models import MissionRecord, MissionRecordPhoto
from members.models import Member
from vehicles.models import Vehicle
from django.utils.translation import gettext_lazy as _

class MissionRecordForm(forms.ModelForm):
    class Meta:
        model = MissionRecord

        fields = [
            'mission_number', 'date', 'time', 'departure', 'destination',
            'vehicle', 'driver_name', 'assistant_1', 'assistant_2',
            'patient_type', 'patient_name', 'patient_age', 'notes',
            'donation_received', 'mission_expenses', 'fuel_cost',
            ]
        widgets = {
            'mission_number': forms.TextInput(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'departure': forms.TextInput(attrs={'class': 'form-input'}),
            'destination': forms.TextInput(attrs={'class': 'form-input'}),
            'vehicle': forms.Select(attrs={'class': 'form-input'}),
            'driver_name': forms.Select(attrs={'class': 'form-input'}),
            'assistant_1': forms.Select(attrs={'class': 'form-input'}),
            'assistant_2': forms.Select(attrs={'class': 'form-input'}),
            'patient_type': forms.TextInput(attrs={'class': 'form-input'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-input'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows':3, 'class': 'form-input'}),
            'donation_received': forms.NumberInput(attrs={'class': 'form-input'}),
            'mission_expenses': forms.NumberInput(attrs={'class': 'form-input'}),
            'fuel_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            }

        labels = {
            'mission_number': _('Mission Number'),
            'date': _('Date'),
            'time': _('Time'),
            'departure': _('Departure'),
            'destination': _('Destination'),
            'vehicle': _('Vehicle'),
            'driver_name': _('Driver Name'),
            'assistant_1': _('Assistant 1'),
            'assistant_2': _('Assistant 2'),
            'patient_type': _('Patient Type'),
            'patient_name': _('Patient Name'),
            'patient_age': _('Patient Age'),
            'notes': _('Notes'),
            'donation_received': _('Donation Received'),
            'mission_expenses': _('Mission Expenses'),
            'fuel_cost': _('Fuel Cost')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver_name'].queryset = Member.objects.filter(is_active=True).order_by('member_id')
        self.fields['assistant_1'].queryset = Member.objects.filter(is_active=True).order_by('member_id')
        self.fields['assistant_2'].queryset = Member.objects.filter(is_active=True).order_by('member_id')
        
        vehicle_queryset = Vehicle.objects.filter(mission_status='Stand-by')
        
        if self.instance.pk:
            vehicle_queryset |= Vehicle.objects.filter(pk=self.instance.vehicle.pk)

        self.fields['vehicle'].queryset = vehicle_queryset

MissionRecordPhotoFormSet = inlineformset_factory (
    parent_model = MissionRecord,
    model = MissionRecordPhoto,
    fields = ('mission', 'image',),
    extra = 3,
    can_delete = True
    )