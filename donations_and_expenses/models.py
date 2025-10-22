from django.db import models
from members.models import Member

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
