from django.db import models
from contracts.models import Contract


class UtilityReading(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="utility_readings"
    )

    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    old_electric = models.PositiveIntegerField()
    new_electric = models.PositiveIntegerField()

    old_water = models.PositiveIntegerField()
    new_water = models.PositiveIntegerField()

    electric_price = models.DecimalField(max_digits=10, decimal_places=2, default=3500)
    water_price = models.DecimalField(max_digits=10, decimal_places=2, default=15000)

    def electric_fee(self):
        return (self.new_electric - self.old_electric) * self.electric_price

    def water_fee(self):
        return (self.new_water - self.old_water) * self.water_price


class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = "UNPAID", "Chưa thanh toán"
        PAID = "PAID", "Đã thanh toán"
        OVERDUE = "OVERDUE", "Quá hạn"

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    room_fee = models.DecimalField(max_digits=12, decimal_places=2)
    electric_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    water_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNPAID
    )