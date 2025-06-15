from django import forms
from .models import Appointment
from users.models import User

class AppointmentCreationForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='DOCTOR').order_by('last_name'),
        label="Choisir un médecin",
        # On utilise une fonction lambda pour afficher "Dr. Nom Prénom (Spécialité)"
        to_field_name='id', # id du docteur
        empty_label="Sélectionnez un spécialiste"
    )
    appointment_date = forms.DateTimeField(
        label="Date et heure souhaitées",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez brièvement le motif de votre consultation...'}),
        }

    # surcharge du constructeur pour personnaliser l'affichage du nom du médecin
    def __init__(self, *args, **kwargs):
        super(AppointmentCreationForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.get_full_name()} ({obj.specialty or 'Généraliste'})"