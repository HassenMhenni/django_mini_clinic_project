from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    """
    Ce formulaire est utilisé pour créer et modifier des instances du modèle Patient.
    Il hérite de forms.ModelForm, ce qui facilite la création de formulaires liés à des modèles.
    """
    class Meta:
        """
        metadata, Elle contient des informations sur le modèle à utiliser, les champs du modèle à inclure dans le formulaire.
        """
        model = Patient
        # Les champs seront affichés dans le formulaire dans l'ordre de cette liste
        fields = ['name', 'date_of_birth', 'contact_info', 'basic_medical_history']
        # Ne pas inclure 'verified_by_admin' ici afin qu'il ne puisse être défini que par l'administrateur.