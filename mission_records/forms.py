from django import forms
from django.forms import inlineformset_factory
from .models import MissionRecord, MissionRecordPhoto, MissionFuelRefill
from members.models import Member
from vehicles.models import Vehicle
from django.utils.translation import gettext_lazy as _


class FuelVoucherInput(forms.ClearableFileInput):
    template_name = 'mission_records/widgets/fuel_voucher_input.html'


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


MISSION_FIELD_ICONS = {
    'mission_number': 'bi-hash',
    'date': 'bi-calendar3',
    'time': 'bi-clock',
    'departure': 'bi-geo-alt',
    'destination': 'bi-pin-map',
    'vehicle': 'bi-truck-front',
    'driver_name': 'bi-person-badge',
    'assistant_1': 'bi-people',
    'assistant_2': 'bi-people',
    'patient_type': 'bi-heart-pulse',
    'patient_name': 'bi-person',
    'patient_age': 'bi-calendar-heart',
    'notes': 'bi-chat-left-text',
    'donation_received': 'bi-cash-coin',
    'mission_expenses': 'bi-receipt',
}


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
            'mission_number': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-input mission-control',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time', 'class': 'form-input mission-control',
            }),
            'departure': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-input mission-control'}),
            'driver_name': forms.Select(attrs={'class': 'form-input mission-control'}),
            'assistant_1': forms.Select(attrs={'class': 'form-input mission-control'}),
            'assistant_2': forms.Select(attrs={'class': 'form-input mission-control'}),
            'patient_type': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-input mission-control'}),
            'notes': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-input mission-control',
            }),
            'donation_received': forms.NumberInput(attrs={'class': 'form-input mission-control'}),
            'mission_expenses': forms.NumberInput(attrs={'class': 'form-input mission-control'}),
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
        for field_name, icon_class in MISSION_FIELD_ICONS.items():
            self.fields[field_name].widget.icon_class = icon_class

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
    FIELD_ICONS = {
        'time': 'bi-clock',
        'pump_name': 'bi-fuel-pump',
        'liters': 'bi-speedometer2',
        'fuel_type': 'bi-droplet-half',
        'cost': 'bi-cash-coin',
        'notes': 'bi-chat-left-text',
        'fuel_voucher_photo': 'bi-camera',
    }

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
            'time': forms.TimeInput(attrs={
                'type': 'time', 'class': 'form-input mission-control',
            }),
            'pump_name': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'liters': forms.NumberInput(attrs={
                'class': 'form-input mission-control', 'min': '0.01', 'step': '0.01',
            }),
            'fuel_type': forms.RadioSelect(attrs={'class': 'fuel-type-radio'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-input mission-control', 'min': '0', 'step': '1',
            }),
            'notes': forms.TextInput(attrs={'class': 'form-input mission-control'}),
            'fuel_voucher_photo': FuelVoucherInput(attrs={
                'class': 'fuel-voucher-input',
                'accept': 'image/*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, icon_class in self.FIELD_ICONS.items():
            self.fields[field_name].widget.icon_class = icon_class


MissionFuelRefillFormSet = inlineformset_factory(
    MissionRecord,
    MissionFuelRefill,
    form=MissionFuelRefillForm,
    extra=1,
    can_delete=True,
)