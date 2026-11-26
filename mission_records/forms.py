from django import forms
from django.forms import inlineformset_factory
from .models import MissionRecord, MissionRecordPhoto, MissionFuelRefill
from members.models import Member
from vehicles.models import Vehicle
from django.utils.translation import gettext_lazy as _, get_language
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
    'patient_type': 'bi-clipboard2-pulse',
    'patient_name': 'bi-person',
    'patient_age': 'bi-calendar-heart',
    'notes': 'bi-chat-left-text',
    'donation_received': 'bi-cash-coin',
    'mission_expenses': 'bi-receipt',
}

PATIENT_TYPE_LABELS = [
    ('Hospital Admission Patient', 'Hospital Admission Patient', 'ဆေးရုံတက်လူနာ'),
    ('Hospital Discharge Patient', 'Hospital Discharge Patient', 'ဆေးရုံဆင်းလူနာ'),
    ('Returning Home Patient', 'Returning Home Patient', 'နေရပ်ပြန်လူနာ'),
    ('Accident Patient', 'Accident Patient', 'အက်စီးဒန့်လူနာ'),
    ('Deceased (DB)', 'Deceased (DB)', 'ကွယ်လွန်သူရုပ်ကလာပ်'),
    ('Mental Health Patient', 'Mental Health Patient', 'စိတ်ကျန်းမာရေးချို့တဲ့လူနာ'),
    ('Substance Withdrawal Patient', 'Substance Withdrawal Patient', 'မူးယစ်ဆေးဖြတ်လူနာ'),
    ('Clinic Patient', 'Clinic Patient', 'ဆေးခန်းပြလူနာ'),
    ('Hospital Transfer Patient', 'Hospital Transfer Patient', 'ဆေးရုံပြောင်းလူနာ'),
    ('Maternity Patient', 'Maternity Patient', 'မီးဖွားလူနာ'),
    ('Emergency Patient', 'Emergency Patient', 'အရေးပေါ်လူနာ'),
    ('Injury Patient', 'Injury Patient', 'ဒဏ်ရာရလူနာ'),
    ('Pediatric Patient', 'Pediatric Patient', 'ကလေးလူနာ'),
    ('Follow-up Patient', 'Follow-up Patient', 'ရက်ချိန်းလူနာ'),
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
                'placeholder': 'ခေါ်ဆောင်သည့်နေရာ',
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-input mission-control',
                'placeholder': 'ပို့ဆောင်မည့်နေရာ',
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
        use_burmese = (get_language() or '').lower().startswith('my')
        patient_choices = [
            (value, burmese if use_burmese else english)
            for value, english, burmese in PATIENT_TYPE_LABELS
        ]
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
        self.fields['patient_type'].widget.icon_class = MISSION_FIELD_ICONS['patient_type']

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
        self.fields['driver_name'].empty_label = None
        self.fields['assistant_1'].empty_label = _('Select assistant 1')
        self.fields['assistant_2'].empty_label = _('Select assistant 2')

        vehicle_queryset = Vehicle.objects.filter(
            mission_status='Stand-by'
        ).order_by('vehicle_id')

        if self.instance.pk:
            vehicle_queryset |= Vehicle.objects.filter(
                pk=self.instance.vehicle.pk
            )

        self.fields['vehicle'].queryset = vehicle_queryset
        self.fields['vehicle'].empty_label = None

        if not self.instance.pk:
            if driver_member and self.fields['driver_name'].queryset.filter(
                pk=driver_member.pk
            ).exists():
                self.initial['driver_name'] = driver_member.pk
            first_available_vehicle = self.fields['vehicle'].queryset.first()
            if first_available_vehicle:
                self.initial['vehicle'] = first_available_vehicle.pk

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
    extra=0,
    can_delete=True,
)