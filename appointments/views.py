
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from appointments.models import Appointment
from .forms import AppointmentCreationForm
from users.decorators import patient_required

from django.http import HttpResponseForbidden # Pour interdire l'accès

from django.views.decorators.http import require_POST



@login_required
@patient_required


###########     CREATE        #################
def create_appointment_view(request):
    if request.method == 'POST':
        form = AppointmentCreationForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False) # Ne sauvegarde pas encore en base de données
            # Assigne le patient connecté à l'instance du rendez-vous
            appointment.patient = request.user # Assigne le patient connecté
            appointment.status = 'PENDING' # statut par défaut
            appointment.save() # sauvegarde
            
            messages.success(request, f"Your appointment request with Dr. {appointment.doctor.last_name} has been successfully submitted. You will receive a notification after confirmation.")
            return redirect('users:patient_dashboard')
        else:
            messages.error(request, "Please correct any errors in the form.")
    else:
        form = AppointmentCreationForm()
        
    context = {
        'form': form,
        'page_title': 'Take an appointment'
    }
    return render(request, 'appointments/appointment_form.html', context)


###########     UPDATE        #################
def update_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)# Recupère le rdv du patient connecté
    if appointment.status != 'PENDING':
        messages.error(request, "This appointment can no longer be modified because it has already been processed.")
        return redirect('users:patient_dashboard')
    if request.method == 'POST':
        # On passe 'instance=appointment' pour dire au formulaire qu'on modifie un objet existant
        form = AppointmentCreationForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been successfully changed.")
            return redirect('users:patient_dashboard')
    else:
        form = AppointmentCreationForm(instance=appointment)


    context = {
        'form': form,
        'page_title': 'Change my appointment'
    }
    return render(request, 'appointments/appointment_form.html', context)


###########     DELETE        #################
def delete_appointment_view(request, pk):
    if request.method != 'POST':
        return HttpResponseForbidden("Method not permitted.")
    
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)

    if appointment.status != 'PENDING':
        messages.error(request, "This appointment can no longer be cancelled as it has already been processed.")
        return redirect('users:patient_dashboard')
    appointment.delete()
    
    messages.success(request, "The appointment has been successfully cancelled.")
    return redirect('users:patient_dashboard')


###############  Processus de validation ou de refus le docteur #####################
def process_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user)
    
    if appointment.status != 'PENDING':
        messages.warning(request, "This request has already been processed.")
        return redirect('users:doctor_dashboard')

    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/process_appointment.html', context)


###############   Validation du rdv par le docteur #####################
@require_POST # Sécurité : cette action ne peut être déclenchée que par une requête POST
def confirm_appointment_action(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user)
    
    if appointment.status == 'PENDING':
        appointment.status = 'CONFIRMED'
        appointment.save()
        messages.success(request, f"The appointment with {appointment.patient.get_full_name()} has been confirmed.")
    else:
        messages.error(request, "The action could not be performed (status is no longer 'Pending').")
        
    return redirect('users:doctor_dashboard')


###############   Refus du rdv par le docteur #####################
@require_POST
def refuse_appointment_action(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user)

    if appointment.status == 'PENDING':
        appointment.status = 'CANCELED' 
        appointment.save()
        messages.info(request, f"The request for {appointment.patient.get_full_name()} was denied.")
    else:
        messages.error(request, "The action could not be performed.")
        
    return redirect('users:doctor_dashboard')
