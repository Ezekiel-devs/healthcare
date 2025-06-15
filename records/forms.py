# records/forms.py
from django import forms

from appointments.models import Appointment
from .models import MedicalRecord, Prescription, LabResult

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['medical_history', 'allergies']
        labels = {
            'medical_history': "Antécédents Médicaux",
            'allergies': "Allergies connues",
        }
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 5}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'instructions', 'appointment']
    
    def __init__(self, *args, **kwargs):
        # On récupère l'ID du patient passé depuis la vue
        patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)
        if patient_id:
            # On filtre le champ 'appointment' pour ne montrer que les RDV de ce patient
            self.fields['appointment'].queryset = Appointment.objects.filter(patient_id=patient_id)

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['title', 'result_date', 'attachment', 'notes']
        widgets = {
            'result_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


# Le __init__ personnalisé dans PrescriptionForm est une amélioration. Il permet de s'assurer que quand le médecin crée une ordonnance, 
# la liste déroulante des rendez-vous ne montre que les rendez-vous du patient concerné, ce qui évite les erreurs.