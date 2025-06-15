from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les rendez-vous.
    """
    # Colonnes à afficher dans la liste des rendez-vous
    list_display = (
        'id', 
        'patient', 
        'doctor', 
        'appointment_date', 
        'status'
    )
    
    # Filtres disponibles sur le côté droit
    list_filter = (
        'status', 
        'doctor',
        'appointment_date'
    )
    
    # Champs sur lesquels on peut faire une recherche
    search_fields = (
        'patient__first_name', 
        'patient__last_name', 
        'doctor__first_name', 
        'doctor__last_name',
        'reason'
    )

    # Pour les champs ForeignKey (patient, doctor), Django affiche une liste déroulante.
    # Pour des milliers d'utilisateurs, c'est lent. 
    # raw_id_fields est plus performant, Il affiche une loupe pour chercher et sélectionner l'utilisateur.
    raw_id_fields = ('patient', 'doctor')

    # Organiser le formulaire d'édition
    fieldsets = (
        (None, {
            'fields': ('patient', 'doctor')
        }),
        ('Détails du rendez-vous', {
            'fields': ('appointment_date', 'reason', 'status')
        }),
    )

    # Champs en lecture seule (gérés automatiquement)
    readonly_fields = ('created_at',)