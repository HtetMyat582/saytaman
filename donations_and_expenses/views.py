from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from members.access import dashboard_access_required
from .forms import FuelRefillForm
from .models import FuelRefill


@dashboard_access_required
def fuel_refill_list(request):
    refills = FuelRefill.objects.select_related(
        'vehicle', 'created_by'
    ).order_by('-date', '-time')

    page_obj = Paginator(refills, 25).get_page(request.GET.get('page'))

    return render(request, 'donations_and_expenses/fuel_refill_list.html', {
        'page_obj': page_obj,
        'now': timezone.localdate().year,
    })


@dashboard_access_required
def fuel_refill_detail(request, pk):
    refill = get_object_or_404(
        FuelRefill.objects.select_related('vehicle', 'created_by'),
        pk=pk,
    )
    return render(request, 'donations_and_expenses/fuel_refill_detail.html', {
        'refill': refill,
    })


@dashboard_access_required
def fuel_refill_add(request):
    if request.method == 'POST':
        form = FuelRefillForm(request.POST, request.FILES)
        if form.is_valid():
            refill = form.save(commit=False)
            refill.created_by = request.user.member_profile
            refill.save()
            messages.success(request, 'Fuel refill recorded.')
            return redirect('fuel_refill_list')
    else:
        form = FuelRefillForm()

    return render(request, 'donations_and_expenses/fuel_refill_form.html', {
        'form': form,
        'now': timezone.localdate().year,
    })


@dashboard_access_required
def fuel_refill_edit(request, pk):
    refill = get_object_or_404(FuelRefill, pk=pk)
    if request.method == 'POST':
        form = FuelRefillForm(request.POST, request.FILES, instance=refill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fuel refill updated.')
            return redirect('fuel_refill_list')
    else:
        form = FuelRefillForm(instance=refill)

    return render(request, 'donations_and_expenses/fuel_refill_form.html', {
        'form': form,
        'refill': refill,
        'now': timezone.localdate().year,
    })


@dashboard_access_required
def fuel_refill_delete(request, pk):
    refill = get_object_or_404(FuelRefill, pk=pk)
    if request.method == 'POST':
        refill.delete()
        messages.success(request, 'Fuel refill deleted.')
    return redirect('fuel_refill_list')
