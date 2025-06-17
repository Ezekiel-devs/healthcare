from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import User
from .forms import PatientRegistrationForm, LoginForm, ProfileUpdateForm
from .decorators import patient_required, doctor_required
from appointments.models import Appointment
from records.models import Prescription, MedicalRecord, LabResult
from records.forms import MedicalRecordForm, PrescriptionForm, LabResultForm 
from django.utils import timezone
from django.db.models import Q

from itertools import groupby

def register_patient_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            MedicalRecord.objects.create(patient=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('users:dashboard-redirect')
    else:
        form = PatientRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        # On passe 'instance=request.user' pour pré-remplir le formulaire avec les données actuelles
        # On passe 'request.FILES' pour gérer le téléversement de la photo
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('users:profile_update') 
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    context = {
        'form': form,
        'page_title': 'Edit my profile'
    }
    return render(request, 'users/profile_form.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:dashboard-redirect')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:home')

@login_required
def dashboard_redirect_view(request):
    if request.user.role == 'PATIENT':
        return redirect('users:patient_dashboard')
    elif request.user.role == 'DOCTOR':
        return redirect('users:doctor_dashboard')
    return redirect('core:home')



########################" PATIENT" ############################

@login_required 
@patient_required
def patient_dashboard_view(request):
    """
    Affiche le tableau de bord pour le patient connecté.
    """
    patient = request.user

    now = timezone.now() #
    # Récupérer les rendez-vous à venir (date > maintenant)
    # On les trie par ordre chronologique (le plus proche en premier)
    upcoming_appointments = Appointment.objects.filter(
        patient=patient, 
        appointment_date__gte=now
    ).order_by('appointment_date')

    # Récupérer les consultations passées (date < maintenant)
    # On les trie par ordre anti-chronologique (la plus récente en premier)
    past_appointments = Appointment.objects.filter(
        patient=patient, 
        appointment_date__lt=now,
        status='COMPLETED'
    ).order_by('-appointment_date')

    # On trie les ordonnances pour afficher les plus récentes en premier
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
    lab_results = LabResult.objects.filter(patient=request.user)
    
    # Récupération du dossier médical
    medical_record = get_object_or_404(MedicalRecord, patient=patient)


    context = {
        'upcoming_appointments': upcoming_appointments, 
        'past_appointments': past_appointments,
        'prescriptions': prescriptions,
        'lab_results': lab_results, 
        'medical_record': medical_record,
        'page_title': 'My Dashboard' 
    }

    return render(request, 'users/patient_dashboard.html', context)


########################" dctor" ############################

# @login_required
# @doctor_required
def doctor_dashboard_view(request):
    doctor = request.user
    

    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    
    My_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__range=(today_start, today_end),
        status='CONFIRMED'
    ).order_by('appointment_date')
    
        # LES DEMANDES EN ATTENTE
    pending_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='PENDING'
    ).order_by('appointment_date') # On les trie par date demandée

    patient_ids = Appointment.objects.filter(doctor=doctor).values_list('patient_id', flat=True).distinct()
    my_patients = User.objects.filter(id__in=patient_ids).order_by('last_name', 'first_name')
    search_query = request.GET.get('q', '')
    if search_query:
        my_patients = my_patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'page_title': 'Doctor Dashboard',
        'My_appointments': My_appointments,
        'pending_appointments': pending_appointments,
        'my_patients': my_patients,
        'search_query': search_query,
    }

    return render(request, 'users/doctor_dashboard.html', context)


########################
def patient_profile_view_for_doctor(request, pk):
    # On récupère le patient par son ID
    patient = get_object_or_404(User, pk=pk, role='PATIENT')
    
    # Vérification de sécurité : le médecin a-t-il le droit de voir ce patient ?
    # On vérifie si ce patient a déjà eu au moins un RDV avec ce médecin.
    if not Appointment.objects.filter(patient=patient, doctor=request.user).exists():
        messages.error(request, "You are not authorized to view this patient record.")
        return redirect('users:doctor_dashboard')

    # Récupérer le dossier médical
    try:
        medical_record = MedicalRecord.objects.get(patient=patient)
    except MedicalRecord.DoesNotExist:
        medical_record = None

    context = {
        'patient': patient,
        'medical_record': medical_record,
    }
    return render(request, 'users/patient_profile_for_doctor.html', context)

################## Planing

def doctor_schedule_view(request):
    doctor = request.user
    now = timezone.now()

    # Récupération de tous les rendez-vous futurs confirmés
    all_future_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='CONFIRMED',
        appointment_date__gte=now
    ).order_by('appointment_date')

    # Groupage des rendez-vous par jour
    # groupby de itertools : Elle prend une liste triée et une fonction "clé" (ici, la date du rdv) et retourne des paires (clé, groupe_d_objets).
    appointments_by_day = {
        key: list(group)
        for key, group in groupby(all_future_appointments, key=lambda app: app.appointment_date.date())
    }

    context = {
        'page_title': 'My Planning',
        'appointments_by_day': appointments_by_day,
    }

    return render(request, 'users/doctor_schedule.html', context)


####### RECORD: Prescription ----- Lab result##############"
def patient_profile_view_for_doctor(request, pk):
    patient = get_object_or_404(User, pk=pk, role='PATIENT')
    # ... (Vérification de sécurité) ...

    medical_record, created = MedicalRecord.objects.get_or_create(patient=patient)

    # Instanciation des formulaires
    record_form = MedicalRecordForm(instance=medical_record)
    # On passe patient_id pour le filtrage intelligent
    prescription_form = PrescriptionForm(patient_id=patient.pk) 
    lab_result_form = LabResultForm()

    if request.method == 'POST':
        # Déterminer quel formulaire a été soumis
        if 'update_record' in request.POST:
            record_form = MedicalRecordForm(request.POST, instance=medical_record)
            if record_form.is_valid():
                record_form.save()
                messages.success(request, "Updated medical file.")
                return redirect('users:patient_profile', pk=patient.pk)
        
        elif 'add_prescription' in request.POST:
            prescription_form = PrescriptionForm(request.POST, patient_id=patient.pk)
            if prescription_form.is_valid():
                new_item = prescription_form.save(commit=False)
                new_item.patient = patient
                new_item.doctor = request.user
                new_item.save()
                messages.success(request, "Order added.")
                return redirect('users:patient_profile', pk=patient.pk)

        elif 'add_lab_result' in request.POST:
            lab_result_form = LabResultForm(request.POST, request.FILES)
            if lab_result_form.is_valid():
                new_item = lab_result_form.save(commit=False)
                new_item.patient = patient
                new_item.doctor = request.user
                new_item.save()
                messages.success(request, "Analysis result added.")
                return redirect('users:patient_profile', pk=patient.pk)

    # Récupération des sonnées pour affichage (ordering est déjà dans Meta)
    prescriptions = Prescription.objects.filter(patient=patient)
    lab_results = LabResult.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'prescriptions': prescriptions,
        'lab_results': lab_results,
        'record_form': record_form,
        'prescription_form': prescription_form,
        'lab_result_form': lab_result_form,
    }
    return render(request, 'users/patient_profile_for_doctor.html', context)