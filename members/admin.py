from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import DateWidget, CharWidget
from .models import Member

class MemberResource(resources.ModelResource):
    dob = fields.Field(
        column_name='dob',
        attribute='dob',
        widget=DateWidget(format='%d-%m-%Y')  # Custom date format
    )
    regirstration_date = fields.Field(
        column_name='registration_date',
        attribute='registration_date',
        widget=DateWidget(format='%d-%m-%Y')  # Custom date format
    )

    class Meta:
        model = Member
        import_id_fields = ('member_id',)
        fields = (
            'member_id', 'name', 'role', 'nrc', 'dob', 'blood_type',
            'address', 'phone_number', 'registration_date', 'is_active',
            'father_name', 'mother_name', 'husband_or_wife', 'job', 'profile_photo'
        )

    def before_import_row(self, row, **kwargs):
        if 'phone_number' in row:
            row['phone_number'] = row['phone_number'].replace(' ', '')

    def dehydrate_role(self, member):
        return member.role.upper() if member.role else ''

    def dehydrate_profile_photo(self, member):
        return member.profile_photo.url if member.profile_photo else ''

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource
    list_display = (
        'member_id', 'name', 'role', 'nrc', 'dob', 'blood_type',
        'phone_number', 'registration_date', 'is_active'
    )
    list_filter = ('role', 'blood_type', 'is_active', 'registration_date')
    search_fields = ('member_id', 'name', 'nrc', 'phone_number', 'father_name', 'mother_name')
    fieldsets = (
        ('Primary Info', {
            'fields': (
                'member_id', 'name', 'role', 'nrc', 'dob', 'blood_type', 'profile_photo', 'is_active'
            )
        }),
        ('Contact & Address', {
            'fields': (
                'phone_number', 'address'
            )
        }),
        ('Family & Job', {
            'fields': (
                'father_name', 'mother_name', 'husband_or_wife', 'job'
            )
        }),
        ('Registration', {
            'fields': (
                'registration_date',
            )
        }),
    )