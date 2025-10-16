
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Vehicle

class VehicleResource(resources.ModelResource):
    class Meta:
        model = Vehicle

@admin.register(Vehicle)
class VehicleAdmin(ImportExportModelAdmin):
    resource_class = VehicleResource
    list_display = ('vehicle_id', 'license_plate', 'status', 'mission_status')
    list_filter = ('status', 'mission_status')