from django.test import TestCase, Client
from django.urls import reverse
from .models import Appointment
from .forms import AppointmentForm
from patient_app.models import Patient
from django.contrib.auth.models import User
from datetime import date, time

class AppointmentModelTests(TestCase):
    def setUp(self):
        # Création d'un patient de test pour les tests de modèle de rendez-vous
        self.patient = Patient.objects.create(name="Test Patient", date_of_birth=date(2000, 1, 1))

    def test_appointment_creation(self):
        # Teste la création d'un objet Appointment.
        appointment = Appointment.objects.create(
            patient=self.patient,
            date=date(2024, 12, 15),
            time=time(10, 00),
            doctor_name="Dr. Smith"
        )
        self.assertEqual(appointment.patient, self.patient) # Vérifie que le patient associé au rendez-vous est correct.
        self.assertEqual(appointment.date, date(2024, 12, 15)) # Vérifie que la date du rendez-vous est correcte.
        self.assertEqual(appointment.time, time(10, 00)) # Vérifie que l'heure du rendez-vous est correcte.
        self.assertEqual(appointment.doctor_name, "Dr. Smith") # Vérifie que le nom du médecin est correct.
        self.assertEqual(str(appointment), f"Test Patient - 2024-12-15 10:00:00") # Vérifie que la représentation en chaîne de caractères de l'objet est correcte.

class AppointmentFormTests(TestCase):
    def setUp(self):
        # Création d'un patient de test pour les tests de formulaire de rendez-vous
        self.patient = Patient.objects.create(name="Test Patient", date_of_birth=date(2000, 1, 1))

    def test_valid_appointment_form(self):
        # Teste un formulaire de rendez-vous valide.
        form_data = {
            "patient": self.patient.pk,
            "date": "2024-12-15",
            "time": "10:00",
            "doctor_name": "Dr. Smith",
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid()) # Vérifie que le formulaire est valide.

    def test_invalid_appointment_form(self):
        # Teste un formulaire de rendez-vous invalide.
        form_data = {
            "patient": "",  # Patient manquant
            "date": "invalid-date", # Date invalide
            "time" : "invalid-time", # Heure invalide
            "doctor_name": "" # Nom du docteur manquant
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid()) # Vérifie que le formulaire est invalide.
        self.assertEqual(len(form.errors), 4)  # Vérifie le nombre total d'erreurs dans le formulaire == 4.
        self.assertIn("patient", form.errors) # Vérifie que l'erreur "patient" est présente.
        self.assertIn("date", form.errors) # Vérifie que l'erreur "date" est présente.
        self.assertIn("time", form.errors) # Vérifie que l'erreur "time" est présente.
        self.assertIn("doctor_name", form.errors) # Vérifie que l'erreur "doctor_name" est présente.

class AppointmentViewTests(TestCase):
    def setUp(self):
        # Mise en place pour les tests de vues de rendez-vous
        self.client = Client() # Création d'un client de test Django pour les requêtes HTTP.
        self.user = User.objects.create_user(username='testuser', password='testpassword') # Création d'un utilisateur de test.
        self.client.login(username='testuser', password='testpassword') # Connexion de l'utilisateur de test.
        self.patient = Patient.objects.create(name="Test Patient", date_of_birth=date(2000, 1, 1)) # Création d'un patient de test.
        self.appointment = Appointment.objects.create( # Création d'un rendez-vous de test.
            patient=self.patient,
            date=date(2024, 12, 15),
            time=time(10, 00),
            doctor_name="Dr. Smith"
        )

    def test_appointment_list_view(self):
        # Teste la vue qui affiche la liste des rendez-vous.
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 200) # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertIn(self.appointment, response.context['appointments']) # Vérifie que le rendez-vous de test est présent dans la liste des rendez-vous envoyée au template.

    def test_appointment_create_view(self):
        # Teste la vue qui affiche le formulaire de création d'un rendez-vous.
        response = self.client.get(reverse('appointment_create'))
        self.assertEqual(response.status_code, 200) # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertIsInstance(response.context['form'], AppointmentForm) # Vérifie que le formulaire correct (AppointmentForm) est passé au template.

    def test_appointment_create_view_post(self):
        # Teste la vue de création de rendez-vous lors de la soumission d'un formulaire valide.
        new_appointment_data = {
            'patient': self.patient.pk,
            'date': '2024-12-16',
            'time': '14:00',
            'doctor_name': 'Dr. Jones',
        }
        response = self.client.post(reverse('appointment_create'), new_appointment_data)
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).
        self.assertEqual(Appointment.objects.count(), 2) # Vérifie que le nombre de rendez-vous dans la base de données a augmenté de 1.

    def test_appointment_update_view(self):
        # Teste la vue qui affiche le formulaire de mise à jour d'un rendez-vous.
        response = self.client.get(reverse('appointment_update', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 200) # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertIsInstance(response.context['form'], AppointmentForm) # Vérifie que le formulaire correct (AppointmentForm) est passé au template.

    def test_appointment_update_view_post(self):
        # Teste la vue de mise à jour d'un rendez-vous lors de la soumission d'un formulaire valide.
        updated_appointment_data = {
            'patient': self.patient.pk,
            'date': '2024-12-17',
            'time': '15:00',
            'doctor_name': 'Dr. Brown',
        }
        response = self.client.post(reverse('appointment_update', args=[self.appointment.pk]), updated_appointment_data)
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).
        self.appointment.refresh_from_db() # Recharge l'objet rendez-vous depuis la base de données pour avoir les dernières modifications.
        self.assertEqual(self.appointment.date, date(2024, 12, 17)) # Vérifie que la date du rendez-vous a été mise à jour.
        self.assertEqual(self.appointment.time, time(15, 00)) # Vérifie que l'heure du rendez-vous a été mise à jour.
        self.assertEqual(self.appointment.doctor_name, 'Dr. Brown') # Vérifie que le nom du médecin a été mis à jour.

    def test_appointment_delete_view(self):
        # Teste la vue qui affiche la page de confirmation de suppression d'un rendez-vous.
        response = self.client.get(reverse('appointment_delete', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 200) # Vérifie que le statut de la réponse HTTP est 200 (OK).

    def test_appointment_delete_view_post(self):
        # Teste la vue de suppression d'un rendez-vous lors de la soumission du formulaire de confirmation.
        response = self.client.post(reverse('appointment_delete', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).
        self.assertEqual(Appointment.objects.count(), 0) # Vérifie que le rendez-vous a bien été supprimé de la base de données.

    def test_unauthenticated_access(self):
        # Teste l'accès aux vues protégées sans authentification.
        self.client.logout() # Déconnecte l'utilisateur.
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection vers la page de connexion).