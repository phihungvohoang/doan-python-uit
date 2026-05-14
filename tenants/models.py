from django.db import models


class Tenant(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    identity_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name