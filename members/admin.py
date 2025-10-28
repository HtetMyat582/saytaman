from django.contrib import admin, messages
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import DateWidget, CharWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from .models import Member

User = get_user_model()

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


@admin.action(description='Create user accounts for selected members (username=member_id)')
def create_users_for_members(modeladmin, request, queryset):
    created = 0
    linked = 0
    for member in queryset:
        if member.user:
            continue
        user = User.objects.filter(username=member.member_id).first()
        if user:
            existing_member = getattr(user, 'member_profile', None)
            if existing_member and existing_member != member:
                messages.warning(request, f"User {user.username} already linked to another member (member_id: {existing_member.member_id}). Skipped {member.member_id}.")
                continue
            member.user = user
            member.must_change_password = True
            member.save(update_fields=['user', 'must_change_password'])
            linked += 1
            continue
        # create user with a default password
        default_password = settings.SECRET_KEY[:12] if hasattr(settings, 'SECRET_KEY') else 'changeme123'
        user = User.objects.create_user(username=member.member_id, email=member.email or '', password=default_password)
        user.is_active = True
        user.save()
        member.user = user
        member.must_change_password = True
        member.save(update_fields=['user', 'must_change_password'])
        created += 1
        # send password reset email so member can set own password
        if member.email:
            form = PasswordResetForm({'email': member.email})
            form.save(request=request, from_email=settings.DEFAULT_FROM_EMAIL)
    messages.success(request, f"Created {created} users and linked {linked} existing users.")

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource
    list_display = (
        'member_id', 'name', 'role', 'nrc', 'dob', 'blood_type',
        'phone_number', 'email', 'registration_date', 'is_active', 'user'
    )
    list_filter = ('role', 'blood_type', 'is_active', 'registration_date')
    search_fields = ('member_id', 'name', 'nrc', 'phone_number', 'email','father_name', 'mother_name')
    fieldsets = (
        ('Primary Info', {
            'fields': (
                'member_id', 'name', 'role', 'nrc', 'dob', 'blood_type', 'profile_photo', 'is_active'
            )
        }),
        ('Contact & Address', {
            'fields': (
                'phone_number', 'address', 'email'
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
    actions = [create_users_for_members]