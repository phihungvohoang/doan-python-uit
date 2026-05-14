from django.db import models
from properties.models import Property


class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Trống"
        OCCUPIED = "OCCUPIED", "Đã thuê"
        MAINTENANCE = "MAINTENANCE", "Bảo trì"

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="rooms"
    )
    room_number = models.CharField(max_length=50)
    area = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    max_people = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    def __str__(self):
        return f"{self.property.name} - {self.room_number}"