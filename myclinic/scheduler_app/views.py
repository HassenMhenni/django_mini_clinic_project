from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointment_list(request):
    """
    Affiche la liste de tous les rendez-vous, triés par date et heure.
    Utilise select_related pour optimiser les requêtes liées au patient.
    """
    appointments = Appointment.objects.select_related('patient').all().order_by('date', 'time')
    return render(request, 'scheduler_app/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    """
    Crée un nouveau rendez-vous.
    Si la méthode est POST, valide et enregistre le formulaire.
    Sinon, affiche un formulaire vide.
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)  # Crée un formulaire avec les données soumises
        if form.is_valid():  # Vérifie si le formulaire est valide
            form.save()  # Enregistre le nouveau rendez-vous dans la base de données
            return redirect('appointment_list')  # Redirige vers la liste des rendez-vous
    else:
        form = AppointmentForm()  # Crée un formulaire vide pour une nouvelle saisie
    return render(request, 'scheduler_app/appointment_form.html', {'form': form})  # Affiche le formulaire

@login_required
def appointment_update(request, pk):
    """
    Met à jour un rendez-vous existant.
    
    Args:
        pk: La clé primaire (identifiant) du rendez-vous à mettre à jour.
    """
    appointment = get_object_or_404(Appointment, pk=pk)  # Récupère le rendez-vous ou retourne 404
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)  # Met à jour le formulaire avec les données soumises
        if form.is_valid():
            form.save()  # Enregistre les modifications dans la base de données
            return redirect('appointment_list')  # Redirige vers la liste des rendez-vous
    else:
        form = AppointmentForm(instance=appointment)  # Remplit le formulaire avec les données existantes
    return render(request, 'scheduler_app/appointment_form.html', {'form': form})  # Affiche le formulaire mis à jour

@login_required
def appointment_delete(request, pk):
    """
    Supprime un rendez-vous spécifique.
    
    Args:
        pk: La clé primaire (identifiant) du rendez-vous à supprimer.
    """
    appointment = get_object_or_404(Appointment, pk=pk)  # Récupère le rendez-vous ou retourne 404
    if request.method == 'POST':
        appointment.delete()  # Supprime le rendez-vous de la base de données
        return redirect('appointment_list')  # Redirige vers la liste des rendez-vous
    # Rend la template de confirmation de suppression
    return render(request, 'scheduler_app/appointment_confirm_delete.html', {'appointment': appointment})
