from django.db import models


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20)
    model = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    purchase_year = models.IntegerField()

    def __str__(self):
        return self.vehicle_number


class MaintenanceRecord(models.Model):

    SERVICE_TYPES = [
        ('Service', 'Service'),
        ('Repair', 'Repair'),
        ('Oil Change', 'Oil Change'),
        ('General Checkup', 'General Checkup'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPES
    )

    description = models.TextField()

    service_date = models.DateField()

    next_service_date = models.DateField(
        blank=True,
        null=True
    )

    venue = models.CharField(max_length=150)

    mileage = models.IntegerField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return self.vehicle.vehicle_number + " - " + self.service_type


class Expense(models.Model):

    EXPENSE_TYPES = [
        ('Service', 'Service'),
        ('Repair', 'Repair'),
        ('Fuel', 'Fuel'),
        ('Spare Parts', 'Spare Parts'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    expense_type = models.CharField(
        max_length=50,
        choices=EXPENSE_TYPES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expense_date = models.DateField()

    description = models.TextField(blank=True)

    def __str__(self):
        return self.vehicle.vehicle_number + " - " + self.expense_type