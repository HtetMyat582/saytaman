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
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows':3}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit member choices if needed (optional)
        self.fields['driver_name'].queryset = Member.objects.order_by('name')
        self.fields['assistant_1'].queryset = Member.objects.order_by('name')
        self.fields['assistant_2'].queryset = Member.objects.order_by('name')
