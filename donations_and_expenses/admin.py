from math import exp
from django.contrib import admin
from .models import Donation, Expense
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class DonationResource(resources.ModelResource):
    class Meta:
        model = Donation

@admin.register(Donation)
class DonationAdmin(ImportExportModelAdmin):
    resource_class = DonationResource
    list_display = [
        'donor_name', 'amount', 'date', 'donation_type', 'donation_method', 'voucher_number',
        ]
    
    list_filter = [
        'date', 'donation_type', 'donation_method'
        ]

    search_fields = [
        'donor_name', 'donor_address', 'voucher_number']

class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense

@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    resource_class = ExpenseResource
    list_display = [
        'expense_type', 'amount', 'payee_name', 'date', 'item'
        ]
    list_filter = [
        'expense_type', 'payee_name',
        ]
    search_fields = [
        'payee_name', 'voucher_number', 'item', 'expense_type'
        ]