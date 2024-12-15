from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    """
    Ce formulaire est utilisé pour créer et modifier des instances du modèle Appointment.
    Il hérite de forms.ModelForm, ce qui facilite la création de formulaires liés à des modèles.
    """
    class Meta:
        """
        Metadonnées du formulaire.
        - model : Le modèle associé au formulaire.
        - fields : Les champs du modèle à inclure dans le formulaire.
        """
        model = Appointment
        fields = ['patient', 'date', 'time', 'doctor_name']
        # Ne pas inclure 'internal_admin_notes' ici afin qu'il ne puisse être défini que par l'administrateur.
