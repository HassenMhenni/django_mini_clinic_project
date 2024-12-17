import os
import sys
import django
import random
from faker import Faker
from datetime import datetime, timedelta

# Déterminer le chemin absolu du répertoire du projet
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_dir)

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myclinic.settings')
django.setup()

# Importation des modèles Patient et Appointment depuis les applications respectives
from patient_app.models import Patient
from scheduler_app.models import Appointment

def populate_patients(n=50):
    """
    Fonction pour peupler la base de données avec un nombre spécifié de patients.

    Args:
        n (int): Le nombre de patients à créer. Par défaut, 50.
    """
    fake = Faker() # Initialise l'objet Faker pour générer des données factices
    patients = []  # Initialise une liste vide pour stocker les objets Patient
    for _ in range(n): # Boucle pour créer n patients
        # Création d'un objet Patient avec des données factices
        patient = Patient(
            name=fake.name(), # Génère un nom aléatoire
            date_of_birth=fake.date_of_birth(minimum_age=0, maximum_age=90), # Génère une date de naissance aléatoire
            contact_info=fake.phone_number(), # Génère un numéro de téléphone aléatoire
            basic_medical_history=fake.text(max_nb_chars=200),  # Génère un texte aléatoire pour les antécédents médicaux
            verified_by_admin=random.choice([True, False]) # Choisit aléatoirement si le patient est vérifié par l'admin ou non
        )
        patients.append(patient) # Ajoute le patient à la liste
    Patient.objects.bulk_create(patients) # Crée tous les patients en une seule requête pour une meilleure performance
    print(f"{n} patients créés avec succès.") # Affiche un message de succès

def populate_appointments(n=100):
    """
    Fonction pour peupler la base de données avec un nombre spécifié de rendez-vous.

    Args:
        n (int): Le nombre de rendez-vous à créer. Par défaut, 100.
    """
    fake = Faker() # Initialise l'objet Faker pour générer des données factices
    patients = list(Patient.objects.all()) # Récupère tous les patients existants
    if not patients: # Vérifie s'il y a des patients
        print("Aucun patient trouvé. Veuillez d'abord peupler les patients.") # Affiche un message d'erreur si aucun patient n'est trouvé
        return # Sort de la fonction si aucun patient n'est trouvé

    appointments = [] # Initialise une liste vide pour stocker les objets Appointment
    for _ in range(n): # Boucle pour créer n rendez-vous
        patient = random.choice(patients) # Choisit un patient aléatoire parmi les patients existants
        # Générer une date aléatoire dans les 30 prochains jours
        appointment_date = fake.date_between(start_date='today', end_date='+30d')
        # Générer une heure aléatoire entre 8h et 17h
        appointment_time = fake.time(pattern="%H:%M", end_datetime=None)
        doctor_name = fake.name() # Génère un nom de médecin aléatoire

        # Création d'un objet Appointment avec des données factices
        appointment = Appointment(
            patient=patient, # Associe le rendez-vous à un patient
            date=appointment_date, # Date du rendez-vous
            time=appointment_time, # Heure du rendez-vous
            doctor_name=doctor_name, # Nom du médecin
            internal_admin_notes=fake.text(max_nb_chars=100) # Notes internes pour l'admin
        )
        appointments.append(appointment) # Ajoute le rendez-vous à la liste
    Appointment.objects.bulk_create(appointments) # Crée tous les rendez-vous en une seule requête pour une meilleure performance
    print(f"{n} rendez-vous créés avec succès.") 

if __name__ == '__main__':
    print("Début du peuplement de la base de données...")
    populate_patients(50)       # Crée 50 patients
    populate_appointments(100)  # Crée 100 rendez-vous
    print("Peuplement terminé.")


'''
Ce script Python est conçu pour peupler une base de données Django avec des données factices pour les modèles Patient et Appointment. Il utilise la librairie faker pour générer des noms, dates, numéros de téléphone, textes et autres données aléatoires réalistes, et crée ensuite ces enregistrements en masse dans la base de données.
Le script configure l'environnement Django, importe les modèles nécessaires, puis exécute les fonctions de peuplement pour les patients et les rendez-vous.
La librairie faker est une bibliothèque Python qui génère des données factices, mais réalistes, comme des noms, adresses, numéros de téléphone, dates, textes, et bien d'autres types de données. Elle est très utile pour le développement, les tests, et pour peupler des bases de données avec des informations de test.
'''