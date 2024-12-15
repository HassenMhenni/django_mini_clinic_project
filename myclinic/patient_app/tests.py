from django.test import TestCase, Client
from django.urls import reverse
from .models import Patient
from .forms import PatientForm
from django.contrib.auth.models import User
from datetime import date

class PatientModelTests(TestCase):
    def test_patient_creation(self):
        patient = Patient.objects.create(
            name="Test Patient",
            date_of_birth=date(2000, 1, 1),  # Create a date object
        )
        self.assertEqual(patient.name, "Test Patient")
        self.assertEqual(patient.date_of_birth, date(2000, 1, 1)) # compare with a date object
        self.assertFalse(patient.verified_by_admin)
        self.assertEqual(str(patient), "Test Patient")

class PatientFormTests(TestCase):
    def test_valid_patient_form(self):
        form_data = {
            "name": "Test Patient",
            "date_of_birth": "2000-01-01",
            "contact_info": "test@example.com",
            "basic_medical_history": "None",
        }
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_patient_form(self):
        form_data = {
            "name": "",  # Missing name
            "date_of_birth": "invalid-date",  # invalid date format
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn("name", form.errors)
        self.assertIn("date_of_birth", form.errors)


class PatientViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.patient = Patient.objects.create(name='Test Patient', date_of_birth=date(2000, 1, 1)) #create date object

    def test_patient_list_view(self):
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.patient, response.context['patients'])
        
    def test_patient_detail_view(self):
         response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.context['patient'], self.patient)

    def test_patient_create_view(self):
        response = self.client.get(reverse('patient_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PatientForm)
    
    def test_patient_create_view_post(self):
        new_patient_data = {
            'name': 'New Patient',
            'date_of_birth': '2001-01-01',
        }
        response = self.client.post(reverse('patient_create'), new_patient_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Patient.objects.count(), 2)

    def test_patient_update_view(self):
        response = self.client.get(reverse('patient_update', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PatientForm)

    def test_patient_update_view_post(self):
         updated_patient_data = {
            'name': 'Updated Patient',
            'date_of_birth': '2002-02-02',
        }
         response = self.client.post(reverse('patient_update', args=[self.patient.pk]), updated_patient_data)
         self.assertEqual(response.status_code, 302)
         self.patient.refresh_from_db()
         self.assertEqual(self.patient.name, 'Updated Patient')
         self.assertEqual(self.patient.date_of_birth, date(2002, 2, 2)) # compare with a date object
    
    def test_patient_delete_view(self):
         response = self.client.get(reverse('patient_delete', args=[self.patient.pk]))
         self.assertEqual(response.status_code, 200)

    def test_patient_delete_view_post(self):
        response = self.client.post(reverse('patient_delete', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Patient.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 302)