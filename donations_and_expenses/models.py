from django.db import models
from members.models import Member
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.utils import timezone

class Donation(models.Model):
    DONATION_TYPE_CHOICES = [
        ('ZK', 'Zakat'),
        ('LL', 'Lillah'),
        ('BI', 'Bank Interest'),
        ('Other', 'Other'),
        ]
    DONATION_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Bank Transfer', 'Bank Transfer'),
        ('KBZ Pay', 'KBZ Pay'),
        ('Wave Pay', 'Wave Pay'),
        ('AYA Pay', 'AYA Pay'),
        ('Other', 'Other'),
        ]

    voucher_number = models.CharField(max_length=20, null=True, blank=True)
    donor_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    donor_address = models.CharField(max_length=200, null=True, blank=True)
    item = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    donation_type = models.CharField(max_length=10, choices=DONATION_TYPE_CHOICES, null=True, blank=True)
    donation_method = models.CharField(max_length=20, choices=DONATION_METHOD_CHOICES, null=True, blank=True)
    def __str__(self):
        return f"{self.donor_name} - {self.amount}"

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('Fuel', 'Fuel'),
        ('Car Repairs', 'Car Repairs'),
        ('Medical Supplies', 'Medical Supplies'),
        ('Office Supplies', 'Office Supplies'),
        ('Food', 'Food'),
        ('General Expenses', 'General Expenses'),
        ('Other', 'Other'),
        ]

    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPE_CHOICES, null=False, blank=False)
    voucher_number = models.CharField(max_length=20, null=True, blank=True)
    payee_name = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=0 ,null=True, blank=True)
    item = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.payee_name} - {self.amount} on {self.date}"

    

class FuelRefill(models.Model):
    vehicle = models.ForeignKey(
        'vehicles.Vehicle',
        on_delete=models.PROTECT,
        related_name='fuel_refills',
    )
    FUEL_TYPE_CHOICES = [
        ('Diesel', 'Diesel'),
        ('92-RON', '92-RON'),
        ('95-RON', '95-RON'),
        ('Premium Diesel', 'Premium Diesel'),
    ]
    date = models.DateField(default=timezone.localdate)
    time = models.TimeField()
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
    created_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fuel_refills_recorded',
    )

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.vehicle.vehicle_id} — {self.date} — {self.cost} MMK"
