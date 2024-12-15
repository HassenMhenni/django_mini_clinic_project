from django.db import models
from django.contrib.auth.models import User

# Définition du modèle Patient
class Patient(models.Model):
    '''
    Définit un nouveau modèle nommé Patient.
    models.Model indique que Patient est un modèle Django, qui sera traduit en une table dans la base de données.
    '''
    # Champ pour le nom du patient de type char, limité à 100 caractères
    name = models.CharField(max_length=100)
    # Champ pour la date de naissance du patient de type date
    date_of_birth = models.DateField()
    # Champ optionnel pour les informations de contact, limité à 255 caractères (blank: le champ peut étre laisser vide , null : ca peut etre null dans la base de données)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    # Champ optionnel pour les antécédents médicaux, peut contenir du texte long
    basic_medical_history = models.TextField(blank=True, null=True)
    # Champ booléen pour indiquer si le patient a été vérifié par un administrateur, par défaut à False
    verified_by_admin = models.BooleanField(default=False)  # Admin-only field

    # Méthode pour retourner le nom du patient comme représentation en chaîne de caractères de l'objet
    def __str__(self):
        return self.name