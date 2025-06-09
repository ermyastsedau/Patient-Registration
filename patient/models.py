from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class GenderChoices(models.TextChoices):
    Male = 'M', 'Male'
    Female = 'F', 'Female'

class Patient(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length = 1, choices = GenderChoices.choices)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    email = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.fullname}"

class ProfessionChoices(models.TextChoices):
    DOCTOR = 'DR', 'Doctor'
    NURSE = 'NR', 'Nurse'
    HEALTH_OFFICER = 'HO', 'Health Officer'
    MIDWIFE = 'MW', 'Midwife'

class HCP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    profession = models.CharField(choices = ProfessionChoices.choices)

    def __str__(self):
        return f"{self.fullname}"
    
class MedicalRecordStatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'

class PaymentStatusChoices(models.TextChoices):
    PAID = 'Paid', 'Paid'
    UNPAID = 'Unpaid', 'Unpaid'
    PARTIAL = 'Partial', 'Partial Payment'

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hcp = models.ForeignKey(HCP, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(choices=MedicalRecordStatusChoices.choices)
    payment_status = models.CharField(choices=PaymentStatusChoices.choices)

    