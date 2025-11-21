from django.contrib import admin
from .models import MissionRecord, MissionRecordPhoto
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
        'vehicle', 'driver_name', 'assistant_1', 'assistant_2',
        'patient_type', 'patient_name', 'patient_age',
        'donation_received', 'mission_expenses', 'fuel_cost', 'timestamp', 'created_by'
    ]
    list_filter = [
        'date', 'departure', 'destination', 'vehicle', 'driver_name', 'assistant_1', 'assistant_2', 'created_by'
    ]
    search_fields = [
        'mission_number', 'departure', 'destination', 'patient_name', 'vehicle__vehicle_id',
        'driver_name__name', 'assistant_1__name', 'assistant_2__name', 'created_by__name'
    ]
    fieldsets = (
        ('Mission Info', {
            'fields': (
                'mission_number', 'date', 'time', 'departure', 'destination',
                'vehicle' ,'driver_name', 'assistant_1', 'assistant_2'
            )
        }),
        ('Patient Info', {
            'fields': (
                'patient_type', 'patient_name', 'patient_age', 'notes'
            )
        }),
        ('Financial Info', {
            'fields': (
                'donation_received', 'mission_expenses', 'fuel_cost'
            )
        }),
        ('Additional Info', {
            'fields': (
                'timestamp', 'back_to_hq', 'created_by'
            )
        }),
    )

@admin.register(MissionRecordPhoto)
class MissionRecordPhotoAdmin(ImportExportModelAdmin):
    list_display = ('mission', 'image')