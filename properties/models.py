from django.db import models
from django.conf import settings


class Property(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties"
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField(blank=True)
    total_floors = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name