from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from .models import Vehicle, MaintenanceRecord, Expense


# Home page
def home(request):

    vehicles = Vehicle.objects.all()

    maintenance_records = MaintenanceRecord.objects.all()

    today = timezone.now().date()

    reminder_date = today + timedelta(days=7)

    upcoming_services = MaintenanceRecord.objects.filter(
        next_service_date__gte=today,
        next_service_date__lte=reminder_date
    ).order_by('next_service_date')

    return render(
        request,
        'maintenance/home.html',
        {
            'vehicles': vehicles,
            'maintenance_records': maintenance_records,
            'upcoming_services': upcoming_services
        }
    )


# Display all maintenance records
def maintenance_list(request):

    records = MaintenanceRecord.objects.all().order_by(
        '-service_date'
    )

    return render(
        request,
        'maintenance/maintenance_list.html',
        {
            'records': records
        }
    )


# View one maintenance record
def maintenance_detail(request, id):

    record = get_object_or_404(
        MaintenanceRecord,
        id=id
    )

    return render(
        request,
        'maintenance/maintenance_detail.html',
        {
            'record': record
        }
    )


# Create maintenance record
def maintenance_create(request):

    vehicles = Vehicle.objects.all()

    if request.method == 'POST':

        vehicle_id = request.POST['vehicle']
        service_type = request.POST['service_type']
        description = request.POST['description']
        service_date = request.POST['service_date']
        next_service_date = request.POST['next_service_date']
        venue = request.POST['venue']
        mileage = request.POST['mileage']
        status = request.POST['status']

        vehicle = Vehicle.objects.get(
            id=vehicle_id
        )

        MaintenanceRecord.objects.create(
            vehicle=vehicle,
            service_type=service_type,
            description=description,
            service_date=service_date,
            next_service_date=next_service_date,
            venue=venue,
            mileage=mileage,
            status=status
        )

        return redirect('maintenance_list')

    return render(
        request,
        'maintenance/maintenance_form.html',
        {
            'vehicles': vehicles,
            'record': None
        }
    )


# Edit maintenance record
def maintenance_edit(request, id):

    record = get_object_or_404(
        MaintenanceRecord,
        id=id
    )

    vehicles = Vehicle.objects.all()

    if request.method == 'POST':

        vehicle_id = request.POST['vehicle']

        record.vehicle = Vehicle.objects.get(
            id=vehicle_id
        )

        record.service_type = request.POST['service_type']
        record.description = request.POST['description']
        record.service_date = request.POST['service_date']
        record.next_service_date = request.POST['next_service_date']
        record.venue = request.POST['venue']
        record.mileage = request.POST['mileage']
        record.status = request.POST['status']

        record.save()

        return redirect(
            'maintenance_detail',
            id=record.id
        )

    return render(
        request,
        'maintenance/maintenance_form.html',
        {
            'vehicles': vehicles,
            'record': record
        }
    )


# Delete maintenance record
def maintenance_delete(request, id):

    record = get_object_or_404(
        MaintenanceRecord,
        id=id
    )

    if request.method == 'POST':

        record.delete()

        return redirect('maintenance_list')

    return render(
        request,
        'maintenance/maintenance_confirm_delete.html',
        {
            'record': record
        }
    )


# Maintenance cost summary
def cost_summary(request):

    total_cost = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    service_cost = Expense.objects.filter(
        expense_type='Service'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    repair_cost = Expense.objects.filter(
        expense_type='Repair'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    fuel_cost = Expense.objects.filter(
        expense_type='Fuel'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    spare_parts_cost = Expense.objects.filter(
        expense_type='Spare Parts'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        request,
        'maintenance/cost_summary.html',
        {
            'total_cost': total_cost,
            'service_cost': service_cost,
            'repair_cost': repair_cost,
            'fuel_cost': fuel_cost,
            'spare_parts_cost': spare_parts_cost,
        }
    )