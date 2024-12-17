from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Patient.
    Cette classe définit comment les objets Patient sont affichés et gérés dans l'interface d'administration Django.
    """
    # Les champs à afficher dans la liste des patients
    list_display = ('name', 'date_of_birth', 'verified_by_admin')
    # Les champs par lesquels filtrer la liste des patients
    list_filter = ('verified_by_admin',)
    # Les champs dans lesquels effectuer une recherche de patients
    search_fields = ('name',)
    # Les champs modifiables dans l'interface d'administration (incluant tous les champs du modèle)
    fields = ('name', 'date_of_birth', 'contact_info', 'basic_medical_history', 'verified_by_admin')