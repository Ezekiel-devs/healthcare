from django.db import models
from django.conf import settings

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('CANCELED', 'Annulé'),
        ('COMPLETED', 'Terminé'),
    )
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments', limit_choices_to={'role': 'PATIENT'})
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'role': 'DOCTOR'})
    appointment_date = models.DateTimeField(verbose_name="Date and time of the appointment")
    reason = models.TextField(verbose_name="Pattern")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"RDV de {self.patient.first_name} avec Dr. {self.doctor.last_name} le {self.appointment_date.strftime('%d/%m/%Y %H:%M')}"