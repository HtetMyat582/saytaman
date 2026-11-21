from django import forms
from django.forms import inlineformset_factory
from .models import MissionRecord, MissionRecordPhoto, MissionFuelRefill
from members.models import Member
from vehicles.models import Vehicle
from django.utils.translation import gettext_lazy as _

class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput
    max_files = 10

    def clean(self, data, initial=None):
        if not data:
            return []

        uploads = data if isinstance(data, (list, tuple)) else [data]

        if len(uploads) > self.max_files:
            raise forms.ValidationError(
                _('Select no more than %(max)s photos.'),
                code='max_files',
                params={'max': self.max_files},
            )

        return [
            forms.ImageField.clean(self, upload, initial)
            for upload in uploads
        ]


class MissionRecordForm(forms.ModelForm):
    photos = MultipleImageField(
        required=False,
        label=_('Mission Photos'),
        widget=MultipleImageInput(attrs={
            'accept': 'image/*',
            'class': 'mission-photo-input',
        }),
    )

    class Meta:
        model = MissionRecord
        fields = [
            'mission_number', 'date', 'time', 'departure', 'destination',
            'vehicle', 'driver_name', 'assistant_1', 'assistant_2',
            'patient_type', 'patient_name', 'patient_age', 'notes',
            'donation_received', 'mission_expenses',
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
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'donation_received': forms.NumberInput(attrs={'class': 'form-input'}),
            'mission_expenses': forms.NumberInput(attrs={'class': 'form-input'}),
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver_name'].queryset = Member.objects.filter(
            is_active=True
        ).order_by('member_id')
        self.fields['assistant_1'].queryset = Member.objects.filter(
            is_active=True
        ).order_by('member_id')
        self.fields['assistant_2'].queryset = Member.objects.filter(
            is_active=True
        ).order_by('member_id')

        vehicle_queryset = Vehicle.objects.filter(mission_status='Stand-by')

        if self.instance.pk:
            vehicle_queryset |= Vehicle.objects.filter(
                pk=self.instance.vehicle.pk
            )

        self.fields['vehicle'].queryset = vehicle_queryset

class MissionFuelRefillForm(forms.ModelForm):
    class Meta:
        model = MissionFuelRefill
        fields = ('time', 'pump_name', 'liters', 'fuel_type', 'cost', 'notes', 'fuel_voucher_photo')
        labels = {
            'time': _('Time'),
            'pump_name': _('Pump'),
            'liters': _('Liters'),
            'fuel_type': _('Fuel Type'),
            'cost': _('Cost'),
            'notes': _('Notes'),
            'fuel_voucher_photo': _('Fuel Voucher Photo'),
        }
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'pump_name': forms.TextInput(attrs={'class': 'form-input'}),
            'liters': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0.01', 'step': '0.01',
            }),
            'fuel_type': forms.Select(attrs={'class': 'form-input'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0', 'step': '1',
            }),
            'notes': forms.TextInput(attrs={'class': 'form-input'}),
            'fuel_voucher_photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }


MissionFuelRefillFormSet = inlineformset_factory(
    MissionRecord,
    MissionFuelRefill,
    form=MissionFuelRefillForm,
    extra=1,
    can_delete=True,
)