from django.contrib import admin
from .models import Member, Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('house_number', 'street', 'township', 'city')
    search_fields = ('house_number', 'street', 'township', 'city')
    list_filter = ('city', 'township')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'member_id', 'name', 'role', 'nrc', 'dob', 'blood_type',
        'phone_number', 'registration_date', 'is_active'
    )
    list_filter = ('role', 'blood_type', 'is_active', 'registration_date')
    search_fields = ('member_id', 'name', 'nrc', 'phone_number', 'father_name', 'mother_name')
    readonly_fields = ('registration_date',)
    autocomplete_fields = ['address']
    fieldsets = (
        (None, {
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
 