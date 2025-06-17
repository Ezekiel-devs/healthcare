from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Role")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone number")
    ville = models.CharField(max_length=100, blank=True, null=True, verbose_name="Town")
    specialty = models.CharField(max_length=100, blank=True, null=True, verbose_name="Specialty (if doctor)")

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Profil Photo")

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"