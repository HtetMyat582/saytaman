from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import DisasterEvent, DisasterEventPhoto

@admin.register(DisasterEvent)
class DisasterEventAdmin(ImportExportModelAdmin):
    list_display = ('event_name', 'disaster_type', 'date', 'location', 'timestamp')
    list_filter = ('disaster_type', 'date', 'location')
    search_fields = ('event_name', 'location', 'description')

@admin.register(DisasterEventPhoto)
class DisasterEventPhotoAdmin(ImportExportModelAdmin):
    list_display = ('event', 'image', 'caption')
    list_filter = ('event',)
    search_fields = ('caption',)
