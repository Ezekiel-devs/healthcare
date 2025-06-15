from django.contrib import admin
from .models import MedicalRecord, Prescription

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les dossiers médicaux.
    """
    list_display = ('id', 'patient', 'get_patient_email')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__email')
    raw_id_fields = ('patient',)

    # Fonction pour afficher l'email du patient dans la liste
    @admin.display(description='Email du Patient')
    def get_patient_email(self, obj):
        return obj.patient.email

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'patient', 
        'doctor', 
        'medication_name', 
        'created_at'
    )
    list_filter = ('doctor',)
    search_fields = (
        'patient__first_name', 
        'patient__last_name', 
        'doctor__last_name', 
        'medication_name'
    )
    raw_id_fields = ('patient', 'doctor', 'appointment')
    date_hierarchy = 'created_at' # Ajoute une navigation par date en haut de la liste