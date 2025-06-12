from django.db import models

class Address(models.Model):
    house_number = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    township = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.house_number}, {self.street}, {self.township}, {self.city}"

class Member(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Patron', 'Patron'),
        ('Chairman', 'Chairman'),
        ('Secretary', 'Secretary'),
        ('Joint Secretary', 'Joint Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Auditor', 'Auditor'),
        ('Committee Member', 'Committee Member'),
        ('Member', 'Member'),
        ('Volunteer', 'Volunteer'),
    ]

    member_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, blank=True)
    nrc = models.CharField(max_length=50, unique=True, null=True, blank=True)
    dob = models.DateField(null=False, blank=False)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=False)
    registration_date = models.DateField(auto_now_add=True, null=False, blank=False)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    husband_or_wife = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member_id}, {self.name}"