from django.contrib import admin
from .models import MissionRecord
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MissionRecordResource(resources.ModelResource):
    class Meta:
        model = MissionRecord

@admin.register(MissionRecord)
class MissionRecordAdmin(ImportExportModelAdmin):
    resource_class = MissionRecordResource
    list_display = [
        'mission_number', 'date', 'time', 'departure', 'destination',
        'driver_name', 'assistant_1', 'assistant_2',
        'patient_name', 'patient_age',
        'donation_received', 'mission_expenses', 'fuel_cost', 'timestamp'
    ]
    list_filter = [
        'date', 'departure', 'destination', 'driver_name', 'assistant_1', 'assistant_2'
    ]
    search_fields = [
        'mission_number', 'departure', 'destination', 'patient_name',
        'driver_name__name', 'assistant_1__name', 'assistant_2__name'
    ]
    fieldsets = (
        ('Mission Info', {
            'fields': (
                'mission_number', 'date', 'time', 'departure', 'destination',
                'driver_name', 'assistant_1', 'assistant_2'
            )
        }),
        ('Patient Info', {
            'fields': (
                'patient_name', 'patient_age', 'photo', 'notes'
            )
        }),
        ('Financial Info', {
            'fields': (
                'donation_received', 'mission_expenses', 'fuel_cost'
            )
        }),
    )
