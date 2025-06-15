from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Médecin'),
        ('RECEPTIONIST', 'Réceptionniste'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Rôle")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone")
    ville = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True, verbose_name="Spécialité (si médecin)")

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Photo de profil")

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"