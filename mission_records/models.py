from django.db import models
from members.models import Member
from vehicles.models import Vehicle
import time
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class MissionRecord(models.Model):

    def mission_number_generator():
        latest_record = MissionRecord.objects.all().order_by('mission_number').last()
        new_mission_number = ''

        if latest_record == None:
            new_mission_number = '001' + '/' + time.strftime("%y", time.localtime())
        else:
            new_mission_number = str(int(latest_record.mission_number[:-3]) + 1).zfill(3) + '/' + time.strftime("%y", time.localtime())
        return new_mission_number

    mission_number = models.CharField(max_length=20, null=False, blank=False, unique=True, default=mission_number_generator)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    departure = models.CharField(max_length=100, null=False, blank=False)
    destination = models.CharField(max_length=100, null=False, blank=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle', null=False, blank=False)
    driver_name = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='driver', null=False, blank=False)
    assistant_1 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assistant_1', null=True, blank=True)
    assistant_2 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assistant_2', null=True, blank=True)
    patient_type = models.CharField(max_length=200, null=True, blank=True)
    patient_name = models.CharField(max_length=50, null=True, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(110)])
    notes = models.TextField(null=True, blank=True)
    donation_received = models.PositiveIntegerField(null=True, blank=True)
    mission_expenses = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    back_to_hq = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='mission_created_by', null=False, blank=False)

    def __str__(self):
        return f"Mission {self.mission_number} on {self.date} from {self.departure} to {self.destination}"

    @property
    def total_fuel_cost(self):
        cached_refills = getattr(self, '_prefetched_objects_cache', {}).get('fuel_refills')
        if cached_refills is None:
            refill_total = self.fuel_refills.aggregate(
                total=models.Sum('cost')
            )['total'] or Decimal('0')
        else:
            refill_total = sum(
                (refill.cost for refill in cached_refills),
                Decimal('0'),
            )

        return refill_total

    @property
    def net_income(self):
        return (
            Decimal(self.donation_received or 0)
            - Decimal(self.mission_expenses or 0)
            - self.total_fuel_cost
        )


class MissionRecordPhoto(models.Model):
    mission = models.ForeignKey(MissionRecord, related_name='mission_photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mission_photos/')


class MissionFuelRefill(models.Model):
    FUEL_TYPE_CHOICES = [
        ('Diesel', 'Diesel'),
        ('92-RON', '92-RON'),
        ('95-RON', '95-RON'),
        ('Premium Diesel', 'Premium Diesel'),
    ]  
    mission = models.ForeignKey(
        MissionRecord,
        on_delete=models.CASCADE,
        related_name='fuel_refills',
    )
    time = models.TimeField(null=True, blank=True)
    pump_name = models.CharField(max_length=150)
    liters = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, null=True)
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(Decimal('0'))],
    )
    notes = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('time', 'pk')

    def __str__(self):
        return f"{self.mission.mission_number} — {self.pump_name} — {self.cost} MMK"