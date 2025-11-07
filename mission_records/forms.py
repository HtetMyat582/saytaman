from token import AT
from django import forms
from .models import MissionRecord
from members.models import Member


class MissionRecordForm(forms.ModelForm):
    class Meta:
        model = MissionRecord

        fields = [
            'mission_number', 'date', 'time', 'departure', 'destination',
            'vehicle', 'driver_name', 'assistant_1', 'assistant_2',
            'patient_name', 'patient_age', 'photo', 'notes',
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
            'patient_name': forms.TextInput(attrs={'class': 'form-input'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-input'}),
            'photo':forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows':3, 'class': 'form-input'}),
            'donation_received': forms.NumberInput(attrs={'class': 'form-input'}),
            'mission_expenses': forms.NumberInput(attrs={'class': 'form-input'}),
            'fuel_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit member choices if needed (optional)
        self.fields['driver_name'].queryset = Member.objects.order_by('member_id')
        self.fields['assistant_1'].queryset = Member.objects.order_by('member_id')
        self.fields['assistant_2'].queryset = Member.objects.order_by('member_id')