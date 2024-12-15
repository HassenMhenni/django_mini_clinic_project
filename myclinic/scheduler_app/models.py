from django.db import models
from patient_app.models import Patient

class Appointment(models.Model):
    """
    Définit un nouveau modèle nommé Appointment.
    Chaque rendez-vous est lié à un patient et contient des informations telles que la date, l'heure et le nom du médecin.
    """
    # Clé étrangère vers le modèle Patient. Suppression en cascade si le patient est supprimé.
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # Champ pour la date du rendez-vous de type date.
    date = models.DateField()
    # Champ pour l'heure du rendez-vous de type time.
    time = models.TimeField()
    # Champ pour le nom du médecin, limité à 100 caractères.
    doctor_name = models.CharField(max_length=100)
    # Champ optionnel pour des notes internes réservées à l'administrateur.
    internal_admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet Appointment.
        """
        return f"{self.patient.name} - {self.date} {self.time}"
