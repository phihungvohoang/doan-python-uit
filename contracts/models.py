from django.db import models
from rooms.models import Room
from tenants.models import Tenant


class Contract(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Đang hiệu lực"
        TERMINATED = "TERMINATED", "Đã kết thúc"

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="contracts")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="contracts")

    start_date = models.DateField()
    end_date = models.DateField()
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def __str__(self):
        return f"{self.tenant.full_name} - {self.room.room_number}"