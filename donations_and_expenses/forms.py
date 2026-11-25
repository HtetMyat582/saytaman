from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Donation, Expense, FuelRefill
from shared.forms import (
    CommaIntegerField,
    CurrencyTextInput,
    mark_browser_local_defaults,
)


class CurrencyAdminForm(forms.ModelForm):
    class Media:
        js = ('js/form-inputs.js',)


class DonationAdminForm(CurrencyAdminForm):
    amount = CommaIntegerField(
        max_value=99_999_999,
        required=False,
        min_value=0,
        widget=CurrencyTextInput(attrs={
            'placeholder': 'Donation amount',
        }),
    )

    class Meta:
        model = Donation
        fields = '__all__'


class ExpenseAdminForm(CurrencyAdminForm):
    amount = CommaIntegerField(
        max_value=9_999_999_999,
        required=False,
        min_value=0,
        widget=CurrencyTextInput(attrs={
            'placeholder': 'Expense amount',
        }),
    )

    class Meta:
        model = Expense
        fields = '__all__'


class FuelRefillForm(CurrencyAdminForm):
    cost = CommaIntegerField(
        max_value=999_999_999_999,
        min_value=0,
        label=_('Cost'),
        widget=CurrencyTextInput(attrs={
            'class': 'form-input',
            'placeholder': 'ဥပမာ - 50,000 MMK',
            'min': '0',
        }),
    )

    class Meta:
        model = FuelRefill
        fields = ('vehicle', 'date', 'time', 'pump_name', 'liters', 'fuel_type', 'cost', 'notes', 'fuel_voucher_photo')
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'pump_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Pump name',
            }),
            'liters': forms.NumberInput(attrs={
                'class': 'form-input', 'min': '0.01', 'step': '0.01',
            }),
            'fuel_type': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'မှတ်ချက် - Notes',
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
        self.fields['vehicle'].empty_label = 'STM-1'
        self.fields['liters'].widget.attrs['placeholder'] = 'Liters'
        self.fields['notes'].widget.attrs['placeholder'] = 'မှတ်ချက် - Notes'
        self.fields['fuel_type'].choices = [
            ('', _('Select fuel type')),
            *FuelRefill.FUEL_TYPE_CHOICES,
        ]
        mark_browser_local_defaults(
            self,
            ('date', 'time'),
            clear_initial=('date',),
        )
