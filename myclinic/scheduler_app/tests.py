from django.test import TestCase, Client
from django.urls import reverse
from .models import Appointment
from .forms import AppointmentForm
from patient_app.models import Patient
from django.contrib.auth.models import User
from datetime import date, time

class AppointmentModelTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(name="Test Patient", date_of_birth=date(2000, 1, 1))

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            date=date(2024, 12, 15),
            time=time(10, 00),
            doctor_name="Dr. Smith"
        )
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.date, date(2024, 12, 15))
        self.assertEqual(appointment.time, time(10, 00))
        self.assertEqual(appointment.doctor_name, "Dr. Smith")
        self.assertEqual(str(appointment), f"Test Patient - 2024-12-15 10:00:00")


class AppointmentFormTests(TestCase):
    def setUp(self):
         self.patient = Patient.objects.create(name="Test Patient", date_of_birth=date(2000, 1, 1))
    
    def test_valid_appointment_form(self):
        form_data = {
            "patient": self.patient.pk,
            "date": "2024-12-15",
            "time": "10:00",
            "doctor_name": "Dr. Smith",
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_appointment_form(self):
        form_data = {
            "patient": "",  # Missing patient
            "date": "invalid-date",
            "time" : "invalid-time",
            "doctor_name": ""
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Check the correct number of errors
        self.assertIn("patient", form.errors)
        self.assertIn("date", form.errors)
        self.assertIn("time", form.errors)
        self.assertIn("doctor_name", form.errors)


class AppointmentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.patient = Patient.objects.create(name="Test Patient", date_of_birth=date(2000, 1, 1))
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            date=date(2024, 12, 15),
            time=time(10, 00),
            doctor_name="Dr. Smith"
        )

    def test_appointment_list_view(self):
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.appointment, response.context['appointments'])
    
    def test_appointment_create_view(self):
        response = self.client.get(reverse('appointment_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AppointmentForm)

    def test_appointment_create_view_post(self):
        new_appointment_data = {
            'patient': self.patient.pk,
            'date': '2024-12-16',
            'time': '14:00',
            'doctor_name': 'Dr. Jones',
        }
        response = self.client.post(reverse('appointment_create'), new_appointment_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_appointment_update_view(self):
        response = self.client.get(reverse('appointment_update', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AppointmentForm)

    def test_appointment_update_view_post(self):
          updated_appointment_data = {
            'patient': self.patient.pk,
            'date': '2024-12-17',
            'time': '15:00',
            'doctor_name': 'Dr. Brown',
        }
          response = self.client.post(reverse('appointment_update', args=[self.appointment.pk]), updated_appointment_data)
          self.assertEqual(response.status_code, 302)
          self.appointment.refresh_from_db()
          self.assertEqual(self.appointment.date, date(2024, 12, 17))
          self.assertEqual(self.appointment.time, time(15, 00))
          self.assertEqual(self.appointment.doctor_name, 'Dr. Brown')

    def test_appointment_delete_view(self):
        response = self.client.get(reverse('appointment_delete', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 200)

    def test_appointment_delete_view_post(self):
        response = self.client.post(reverse('appointment_delete', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('appointment_list'))
        self.assertEqual(response.status_code, 302)