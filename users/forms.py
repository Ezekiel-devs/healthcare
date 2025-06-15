from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class PatientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'ville', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'PATIENT' # Assigner le rôle Patient par défaut
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    pass

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone', 'ville', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On peut rendre certains champs non modifiables si on le souhaite
        # self.fields['email'].disabled = True