from django import forms
from django.forms import inlineformset_factory
from .models import MissionRecord, MissionRecordPhoto, MissionFuelRefill
from members.models import Member
from vehicles.models import Vehicle
from django.utils.translation import gettext_lazy as _
from shared.forms import (
    CommaIntegerField,
    CurrencyTextInput,
    mark_browser_local_defaults,
)


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

PATIENT_TYPE_CHOICES = [
    ('Hospital Admission Patient', _('ဆေးရုံတက်လူနာ - Hospital Admission Patient')),
    ('Hospital Discharge Patient', _('ဆေးရုံဆင်းလူနာ - Hospital Discharge Patient')),
    ('Returning Home Patient', _('နေရပ်ပြန်လူနာ - Returning Home Patient')),
    ('Accident Patient', _('အက်စီးဒန့်လူနာ - Accident Patient')),
    ('Deceased (DB)', _('ကွယ်လွန်သူရုပ်ကလာပ် - Deceased (DB)')),
    ('Mental Health Patient', _('စိတ်ကျန်းမာရေးချို့တဲ့လူနာ - Mental Health Patient')),
    ('Substance Withdrawal Patient', _('မူးယစ်ဆေးဖြတ်လူနာ - Substance Withdrawal Patient')),
    ('Clinic Patient', _('ဆေးခန်းပြလူနာ - Clinic Patient')),
    ('Hospital Transfer Patient', _('ဆေးရုံပြောင်းလူနာ - Hospital Transfer Patient')),
    ('Maternity Patient', _('မီးဖွားလူနာ - Maternity Patient')),
    ('Emergency Patient', _('အရေးပေါ်လူနာ - Emergency Patient')),
    ('Injury Patient', _('ဒဏ်ရာရလူနာ - Injury Patient')),
    ('Pediatric Patient', _('ကလေးလူနာ - Pediatric Patient')),
    ('Elderly Patient', _('သက်ကြီးလူနာ - Elderly Patient')),
    ('Follow-up Patient', _('ပြန်လည်စစ်ဆေးရန်လူနာ - Follow-up Patient')),
]


class MissionRecordForm(forms.ModelForm):
    donation_received = CommaIntegerField(
        required=False,
        min_value=0,
        label=_('Donation Received'),
        widget=CurrencyTextInput(attrs={
            'class': 'form-input mission-control',
            'placeholder': 'ဥပမာ - 500,000 MMK',
        }),
    )
    mission_expenses = CommaIntegerField(
        required=False,
        min_value=0,
        label=_('Mission Expenses'),
        widget=CurrencyTextInput(attrs={
            'class': 'form-input mission-control',
            'placeholder': 'ဥပမာ - 100,000 MMK',
        }),
    )
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
            'mission_number': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': '001/26',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-input mission-control',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time', 'class': 'form-input mission-control',
            }),
            'departure': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'ထွက်ခွာမည့်နေရာ',
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'သွားမည့်နေရာ',
            }),
            'vehicle': forms.Select(attrs={'class': 'form-input mission-control'}),
            'driver_name': forms.Select(attrs={'class': 'form-input mission-control'}),
            'assistant_1': forms.Select(attrs={'class': 'form-input mission-control'}),
            'assistant_2': forms.Select(attrs={'class': 'form-input mission-control'}),
            'patient_type': forms.Select(attrs={'class': 'form-input mission-control'}),
            'patient_name': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'လူနာအမည် - Patient name',
            }),
            'patient_age': forms.NumberInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'အသက် - Age',
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'မှတ်ချက် - Notes',
            }),
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

    def __init__(
        self,
        *args,
        can_edit_mission_number=False,
        driver_member=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.fields['mission_number'].disabled = not can_edit_mission_number
        for field_name, icon_class in MISSION_FIELD_ICONS.items():
            self.fields[field_name].widget.icon_class = icon_class

        existing_patient_type = (
            self.initial.get('patient_type') or self.instance.patient_type
        )
        patient_choices = list(PATIENT_TYPE_CHOICES)
        patient_values = {value for value, _label in patient_choices}
        if existing_patient_type and existing_patient_type not in patient_values:
            patient_choices.insert(0, (existing_patient_type, existing_patient_type))
        patient_choices.insert(0, ('', _('Select patient type')))
        patient_type_label = self.fields['patient_type'].label
        self.fields['patient_type'] = forms.ChoiceField(
            choices=patient_choices,
            required=False,
            label=patient_type_label,
            widget=forms.Select(attrs={
                'class': 'form-input mission-control',
            }),
        )

        self.fields['vehicle'].empty_label = 'STM-1'
        if driver_member:
            self.fields['driver_name'].empty_label = (
                f'{driver_member.member_id} - {driver_member.name}'
            )
        else:
            self.fields['driver_name'].empty_label = _('Select driver')
        self.fields['assistant_1'].empty_label = _('Select assistant 1')
        self.fields['assistant_2'].empty_label = _('Select assistant 2')

        self.fields['patient_name'].widget.attrs['placeholder'] = (
            'လူနာအမည် - Patient name'
        )
        self.fields['patient_age'].widget.attrs['placeholder'] = 'အသက် - Age'
        self.fields['notes'].widget.attrs['placeholder'] = 'မှတ်ချက် - Notes'
        mark_browser_local_defaults(self, ('date', 'time'))

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
    cost = CommaIntegerField(
        max_value=999_999_999_999,
        min_value=0,
        label=_('Cost'),
        widget=CurrencyTextInput(attrs={
            'class': 'form-input mission-control',
            'placeholder': 'ဥပမာ - 50,000 MMK',
            'min': '0',
        }),
    )

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
                'class': 'form-input mission-control',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Liters',
            }),
            'fuel_type': forms.RadioSelect(attrs={'class': 'fuel-type-radio'}),
            'notes': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'မှတ်ချက် - Notes',
            }),
            'fuel_voucher_photo': FuelVoucherInput(attrs={
                'class': 'fuel-voucher-input',
                'accept': 'image/*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, icon_class in self.FIELD_ICONS.items():
            self.fields[field_name].widget.icon_class = icon_class
        self.fields['fuel_type'].choices = MissionFuelRefill.FUEL_TYPE_CHOICES
        self.fields['pump_name'].widget.attrs['placeholder'] = 'Pump name'
        self.fields['notes'].widget.attrs['placeholder'] = 'မှတ်ချက် - Notes'
        mark_browser_local_defaults(self, ('time',))


MissionFuelRefillFormSet = inlineformset_factory(
    MissionRecord,
    MissionFuelRefill,
    form=MissionFuelRefillForm,
    extra=1,
    can_delete=True,
)