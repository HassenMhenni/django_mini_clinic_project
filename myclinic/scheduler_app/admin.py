from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Appointment.
    Cette classe définit comment les objets Appointment sont affichés et gérés dans l'interface d'administration Django.
    """
    # Les champs à afficher dans la liste des rendez-vous
    list_display = ('patient', 'date', 'time', 'doctor_name')
    # Les champs par lesquels filtrer la liste des rendez-vous
    list_filter = ('date', 'doctor_name')
    # Les champs dans lesquels effectuer une recherche de rendez-vous
    search_fields = ('patient__name', 'doctor_name')
    # Les champs modifiables dans l'interface d'administration (incluant internal_admin_notes)
    fields = ('patient', 'date', 'time', 'doctor_name', 'internal_admin_notes')