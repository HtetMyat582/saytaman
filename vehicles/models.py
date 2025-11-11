from django.db import models

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Service', 'Service'),
    ]

    MISSION_STATUS_CHOICES = [
        ('On Mission', 'On Mission'),
        ('Stand-by', 'Stand-by'),
        ('Unavailable', 'Unavailable'),
    ]

    vehicle_id = models.CharField(max_length=50, unique=True)
    license_plate = models.CharField(max_length=20, null=True, blank=True)
    license_expiry_date = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    mission_status = models.CharField(max_length=20, choices=MISSION_STATUS_CHOICES, default='Stand-by')
    photo = models.ImageField(upload_to='vehicle_photos/', null=True, blank=True)
    
    def __str__(self):
        if self.status == 'Inactive' or self.status == 'Service':
            self.mission_status = 'Unavailable'

        return f"{self.vehicle_id}"
