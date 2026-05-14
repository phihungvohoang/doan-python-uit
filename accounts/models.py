from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Chủ trọ"
        STAFF = "STAFF", "Nhân viên"
        TENANT = "TENANT", "Người thuê"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OWNER
    )