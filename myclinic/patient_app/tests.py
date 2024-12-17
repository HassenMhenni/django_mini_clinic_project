from django.test import TestCase, Client
from django.urls import reverse
from .models import Patient
from .forms import PatientForm
from django.contrib.auth.models import User
from datetime import date

class PatientModelTests(TestCase):
    def test_patient_creation(self):
        # Teste la création d'un objet Patient.
        patient = Patient.objects.create(
            name="Test Patient",
            date_of_birth=date(2000, 1, 1), 
        )
        self.assertEqual(patient.name, "Test Patient") # Vérifie que le nom du patient est correct.
        self.assertEqual(patient.date_of_birth, date(2000, 1, 1)) # Vérifie que la date de naissance du patient est correcte.
        self.assertFalse(patient.verified_by_admin) # Vérifie que le champ verified_by_admin est False par défaut.
        self.assertEqual(str(patient), "Test Patient") # Vérifie que la représentation en chaîne de caractères de l'objet est correcte.

class PatientFormTests(TestCase):
    def test_valid_patient_form(self):
        # Teste un formulaire de patient valide.
        form_data = {
            "name": "Test Patient",
            "date_of_birth": "2000-01-01",
            "contact_info": "test@example.com",
            "basic_medical_history": "None",
        }
        form = PatientForm(data=form_data) 
        self.assertTrue(form.is_valid())  # Vérifie que le formulaire est valide.
    
    def test_invalid_patient_form(self):
        # Teste un formulaire de patient invalide.
        form_data = {
            "name": "",  # Nom manquant
            "date_of_birth": "invalid-date", # Date de naissance invalide
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid()) # Vérifie que le formulaire est invalide.
        self.assertEqual(len(form.errors), 2) # Vérifie que le nombre total d'erreurs est de 2.
        self.assertIn("name", form.errors) # Vérifie que l'erreur "name" est présente.
        self.assertIn("date_of_birth", form.errors) # Vérifie que l'erreur "date_of_birth" est présente.

class PatientViewTests(TestCase):
    def setUp(self):
        # Mise en place pour les tests de vues de patients.
        self.client = Client() # Création d'un client de test Django pour les requêtes HTTP.
        self.user = User.objects.create_user(username='testuser', password='testpassword') # Création d'un utilisateur de test.
        self.client.login(username='testuser', password='testpassword') # Connexion de l'utilisateur de test.
        self.patient = Patient.objects.create(name='Test Patient', date_of_birth=date(2000, 1, 1)) # Création d'un objet patient de test.

    def test_patient_list_view(self):
        # Vérifie que la vue "patient_list" affiche correctement la liste des patients.
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)  # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertIn(self.patient, response.context['patients'])  # Vérifie que le patient de test est bien présent dans la liste des patients envoyée au template.

    def test_patient_detail_view(self):
        # Vérifie que la vue "patient_detail" affiche correctement les détails d'un patient spécifique (clé primaire).
        response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)  # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertEqual(response.context['patient'], self.patient)  # Vérifie que le patient correct est passé au template.

    def test_patient_create_view(self):
        # Vérifie que la vue "patient_create" affiche correctement le formulaire pour la création d'un nouveau patient.
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 200)  # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertIsInstance(response.context['form'], PatientForm) # Vérifie que le formulaire correct (PatientForm) est passé au template.

    def test_patient_create_view_post(self):
        # Vérifie que la vue patient_create gère correctement une requête POST avec des données valides, en créant un nouveau patient.
        new_patient_data = {
            'name': 'New Patient',
            'date_of_birth': '2001-01-01',
        }
        response = self.client.post(reverse('patient_create'), new_patient_data)
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).
        self.assertEqual(Patient.objects.count(), 2) # Vérifie que le nombre d'enregistrements de patients dans la base de données a augmenté de 1.

    def test_patient_update_view(self):
        # Vérifie que la vue patient_update affiche correctement le formulaire pour la mise à jour d'un patient existant.
        response = self.client.get(reverse('patient_update', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200) # Vérifie que le statut de la réponse HTTP est 200 (OK).
        self.assertIsInstance(response.context['form'], PatientForm) # Vérifie que la variable de contexte form est une instance de PatientForm.

    def test_patient_update_view_post(self):
         # Vérifie que la vue patient_update gère correctement une requête POST avec des données valides, en mettant à jour un patient existant.
         updated_patient_data = {
            'name': 'Updated Patient',
            'date_of_birth': '2002-02-02',
        }
         response = self.client.post(reverse('patient_update', args=[self.patient.pk]), updated_patient_data)
         self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).
         self.patient.refresh_from_db() # Recharge l'objet patient depuis la base de données pour avoir les dernières modifications.
         self.assertEqual(self.patient.name, 'Updated Patient') # Vérifie que le nom du patient a bien été mis à jour.
         self.assertEqual(self.patient.date_of_birth, date(2002, 2, 2)) # Vérifie que la date de naissance du patient a bien été mise à jour.
    
    def test_patient_delete_view(self):
         # Vérifie que la vue patient_delete affiche correctement la page de confirmation pour la suppression d'un patient.
         response = self.client.get(reverse('patient_delete', args=[self.patient.pk]))
         self.assertEqual(response.status_code, 200) # Vérifie que le statut de la réponse HTTP est 200 (OK).

    def test_patient_delete_view_post(self):
        # Vérifie que la vue patient_delete gère correctement une requête POST, en supprimant un patient.
        response = self.client.post(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).
        self.assertEqual(Patient.objects.count(), 0) # Vérifie que le nombre d'enregistrements de patients dans la base de données est 0 après la suppression.

    def test_unauthenticated_access(self):
        # Vérifie que les utilisateurs non authentifiés sont redirigés vers la page de connexion lorsqu'ils essaient d'accéder à une vue protégée (@login_required).
        self.client.logout() # Déconnecte l'utilisateur.
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 302) # Vérifie que le statut de la réponse HTTP est 302 (redirection).