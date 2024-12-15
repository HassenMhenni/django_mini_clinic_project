from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm

# Décorateur @login_required : assure que seules les personnes connectées peuvent accéder à ces vues.
@login_required
def patient_list(request):
    """
    Affiche la liste des patients. Permet également de rechercher des patients par nom.
    """
    # Récupère le paramètre 'q' de la requête GET (utilisé pour la recherche)
    query = request.GET.get('q')
    
    if query:  # Si une requête de recherche est présente
        # Filtre les patients dont le nom contient la chaîne de recherche
        patients = Patient.objects.filter(name__icontains=query)
    else:  # Sinon, affiche tous les patients
        patients = Patient.objects.all()
    
    return render(request, 'patient_app/patient_list.html', {'patients': patients, 'query': query})


@login_required
def patient_detail(request, pk):
    """
    Affiche les détails d'un patient spécifique.

    Args:
        pk: La clé primaire (identifiant) du patient à afficher.
    """
    # Récupère le patient dont la clé primaire est 'pk', ou retourne une erreur 404 si non trouvé.
    patient = get_object_or_404(Patient, pk=pk)
    
    # Rend la template avec les données du patient
    return render(request, 'patient_app/patient_detail.html', {'patient': patient})


@login_required
def patient_create(request):
    """
    Crée un nouveau patient.

    """
    if request.method == 'POST':  # Si le formulaire est soumis
        form = PatientForm(request.POST) # Crée un formulaire avec les données soumises
        if form.is_valid(): # Si le formulaire est valide
            form.save()  # Enregistre le nouveau patient dans la base de données
            return redirect('patient_list')  # Redirige vers la liste des patients
    else:  # Si c'est une requête GET (première visite de la page)
        form = PatientForm()  # Crée un formulaire vide
    
    return render(request, 'patient_app/patient_form.html', {'form': form})


@login_required
def patient_update(request, pk):
    """
    Met à jour les informations d'un patient existant.

    Args:
        pk: La clé primaire (identifiant) du patient à mettre à jour.

    """
    patient = get_object_or_404(Patient, pk=pk) # Récupère le patient, ou retourne 404 si non trouvé
    if request.method == 'POST':  # Si le formulaire est soumis
        form = PatientForm(request.POST, instance=patient) # Crée un formulaire avec les données soumises et le patient existant
        if form.is_valid(): # Si le formulaire est valide
            form.save()  # Met à jour les informations du patient dans la base de données
            return redirect('patient_detail', pk=patient.pk) # Redirige vers la page de détail du patient
    else:  # Si c'est une requête GET (première visite de la page)
        form = PatientForm(instance=patient) # Crée un formulaire pré-rempli avec les données du patient
    
    # Rend la template du formulaire (pour affichage initial ou avec erreurs)
    return render(request, 'patient_app/patient_form.html', {'form': form})


@login_required
def patient_delete(request, pk):
    """
    Supprime un patient.

    Args:
        pk: La clé primaire (identifiant) du patient à supprimer.

    """
    patient = get_object_or_404(Patient, pk=pk)  # Récupère le patient, ou retourne 404 si non trouvé
    if request.method == 'POST':  # Si le formulaire de suppression est soumis
        patient.delete()  # Supprime le patient de la base de données
        return redirect('patient_list')  # Redirige vers la liste des patients
    
    # Rend la template de confirmation de suppression
    return render(request, 'patient_app/patient_confirm_delete.html', {'patient': patient})