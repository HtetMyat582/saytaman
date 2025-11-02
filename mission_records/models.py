from django.db import models
from members.models import Member
from vehicles.models import Vehicle

class MissionRecord(models.Model):
    mission_number = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    departure = models.CharField(max_length=100, null=False, blank=False)
    destination = models.CharField(max_length=100, null=False, blank=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle', null=False, blank=False)
    driver_name = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='driver', null=False, blank=False)
    assistant_1 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assistant_1', null=True, blank=True)
    assistant_2 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assistant_2', null=True, blank=True)
    patient_name = models.CharField(max_length=50, null=True, blank=True)
    patient_age = models.IntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to='mission_photos/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    donation_received = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    mission_expenses = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    fuel_cost = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mission {self.mission_number} on {self.date} from {self.departure} to {self.destination}"

