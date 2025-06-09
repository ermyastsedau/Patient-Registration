from django.contrib.auth.models import AbstractUser
from django.db import models

class RoleChoices(models.TextChoices):
    SYSTEM_ADMIN = 'ADMIN', 'System Admin'
    DOCTOR = 'DOCTOR', 'Doctor'
    RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=RoleChoices.choices)
