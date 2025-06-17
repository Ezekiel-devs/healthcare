from django.db import models
from django.conf import settings
from appointments.models import Appointment

class MedicalRecord(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'PATIENT'})
    medical_history = models.TextField(blank=True, verbose_name="Medical History")
    allergies = models.TextField(blank=True, verbose_name="Allergies")

    def __str__(self):
        return f"{self.patient.get_full_name()} folder"

class Prescription(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions', limit_choices_to={'role': 'PATIENT'})
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issued_prescriptions', limit_choices_to={'role': 'DOCTOR'})
    # Une ordonnance peut être liée à un RDV, mais ce n'est pas obligatoire (ex: renouvellement par téléphone)
    # C'est pourquoi on utilise on_delete=models.SET_NULL, null=True, blank=True
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    medication_name = models.CharField(max_length=200, verbose_name="Medicine")
    dosage = models.CharField(max_length=100, verbose_name="Dosage")
    instructions = models.TextField(verbose_name="Instructions")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class LabResult(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_results', limit_choices_to={'role': 'PATIENT'})
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issued_lab_results', limit_choices_to={'role': 'DOCTOR'})
    title = models.CharField(max_length=200, verbose_name="Title of the analysis")
    result_date = models.DateField(verbose_name="Result date")
    attachment = models.FileField(upload_to='lab_results/%Y/%m/%d/', verbose_name="Fichier joint")
    notes = models.TextField(blank=True, verbose_name="Doctor's Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-result_date'] 

    def __str__(self):
        return f"Result for {self.patient.get_full_name()} - {self.title}"