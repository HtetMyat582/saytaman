from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import DateWidget, ForeignKeyWidget, CharWidget
from .models import Member, Address

class AddressResource(resources.ModelResource):
    class Meta:
        model = Address
        import_id_fields = ('id',)
        fields = ('id', 'house_number', 'street', 'township', 'city')

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    resource_class = AddressResource
    list_display = ('house_number', 'street', 'township', 'city')
    search_fields = ('house_number', 'street', 'township', 'city')
    list_filter = ('city', 'township')

class MemberResource(resources.ModelResource):
    dob = fields.Field(
        column_name='dob',
        attribute='dob',
        widget=DateWidget(format='%d-%m-%Y')  # Custom date format
    )
    address = fields.Field(
        column_name='address',
        attribute='address',
        widget=ForeignKeyWidget(Address, 'id')  # Use Address ID for import/export
    )
    profile_photo = fields.Field(
        column_name='profile_photo',
        attribute='profile_photo',
        widget=CharWidget()
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
        # Example: Clean up phone numbers before import
        if 'phone_number' in row:
            row['phone_number'] = row['phone_number'].replace(' ', '')

    def dehydrate_role(self, member):
        # Example: Export role in uppercase
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
    readonly_fields = ('registration_date',)
    autocomplete_fields = ['address']
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