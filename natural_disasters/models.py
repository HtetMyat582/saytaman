from django.db import models

class DisasterEvent(models.Model):
    DISASTER_TYPE_CHOICES = [
        ('Earthquake', 'Earthquake'),
        ('Flood', 'Flood'),
        ('Hurricane', 'Hurricane'),
        ('Wildfire', 'Wildfire'),
        ('Pandemic', 'Pandemic'),
        ('Landslide', 'Landslide'),
        ('Fire', 'Fire'),
        ('Other', 'Other'),
    ]

    event_name = models.CharField(max_length=100, null=False, blank=False)
    disaster_type = models.CharField(max_length=50, choices=DISASTER_TYPE_CHOICES, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    relief_operations = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.event_name} - {self.disaster_type} on {self.date} at {self.location}"

class DisasterEventPhoto(models.Model):
    event = models.ForeignKey(DisasterEvent, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='disaster_photos/')
    caption = models.CharField(max_length=255, blank=True, null=True)
