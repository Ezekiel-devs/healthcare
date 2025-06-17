from django import forms
from .models import Appointment
from users.models import User

class AppointmentCreationForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='DOCTOR').order_by('last_name'),
        label="Choose a doctor",
        # On utilise une fonction lambda pour afficher "Dr. Nom Prénom (Spécialité)"
        to_field_name='id', # id du docteur
        empty_label="Select a specialist"
    )
    appointment_date = forms.DateTimeField(
        label="Desired date and times",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Briefly describe the reason for your consultation...'}),
        }

    # surcharge du constructeur pour personnaliser l'affichage du nom du médecin
    def __init__(self, *args, **kwargs):
        super(AppointmentCreationForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.get_full_name()} ({obj.specialty or 'Généraliste'})"