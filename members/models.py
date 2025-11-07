from django.db import models
from django.conf import settings

class Member(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A', 'A'), ('A+', 'A+'), ('A-', 'A-'),
        ('B', 'B'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB', 'AB'), ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O', 'O'), ('O+', 'O+'), ('O-', 'O-'),
    ]

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Patron', 'Patron'),
        ('Chairman', 'Chairman'),
        ('Vice Chairman', 'Vice Chairman'),
        ('Secretary', 'Secretary'),
        ('Joint Secretary', 'Joint Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Auditor', 'Auditor'),
        ('Executive Member', 'Executive Member'),
        ('Member', 'Member'),
        ('Volunteer', 'Volunteer'),
    ]

    ADDRESS_CHOICES = [
        ('Aungmyaytharzan', 'Aungmyaytharzan'),
        ('Chanayetharsan', 'Chanayetharsan'),
        ('Mahaaungmyay', 'Mahaaungmyay'),
        ('Pyigyitagon', 'Pyigyitagon'),
        ('Chanmyathazi', 'Chanmyathazi'),
        ('Patheingyi', 'Patheingyi'),
    ]

    member_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, blank=True)
    nrc = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=False, blank=False)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=False)
    address = models.CharField(max_length=50, choices=ADDRESS_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=False)
    email = models.EmailField(null=True, blank=True)
#    registration_date = models.DateField(auto_now_add=False, null=False, blank=False)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    husband_or_wife = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # link to Django user account (nullable until admin creates/links)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='member_profile')

    # flag to require password change after first login
    must_change_password = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member_id}, {self.name}"