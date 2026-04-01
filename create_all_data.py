# Script complet pour créer toutes les données nécessaires pour l'application exams
# Exécutez avec : python manage.py shell < create_all_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

print("Creation de toutes les donnees pour l'application exams...")

# 1. Créer des salles (timetable)
from timetable.models import Salle
salles_data = [
    {"nom": "Salle A101", "capacite": 30, "description": "Salle de cours principale"},
    {"nom": "Salle B205", "capacite": 25, "description": "Salle informatique"},
    {"nom": "Salle C150", "capacite": 40, "description": "Amphithéâtre"},
    {"nom": "Labo Chimie", "capacite": 20, "description": "Laboratoire de chimie"},
]

for salle_data in salles_data:
    salle, created = Salle.objects.get_or_create(nom=salle_data["nom"], defaults=salle_data)
    if created:
        print(f"Salle creee: {salle.nom}")
    else:
        print(f"Salle existe deja: {salle.nom}")

# 2. Créer des enseignants (timetable)
from timetable.models import Enseignant
enseignants_data = [
    {"nom": "Dupont Jean", "email": "dupont@ecole.fr", "telephone": "0123456789", "specialite": "Mathématiques"},
    {"nom": "Marie Sophie", "email": "marie@ecole.fr", "telephone": "0234567890", "specialite": "Physique"},
    {"nom": "Martin Paul", "email": "martin@ecole.fr", "telephone": "0345678901", "specialite": "Informatique"},
    {"nom": "Durand Claire", "email": "durand@ecole.fr", "telephone": "0456789012", "specialite": "Chimie"},
]

for ens_data in enseignants_data:
    enseignant, created = Enseignant.objects.get_or_create(email=ens_data["email"], defaults=ens_data)
    if created:
        print(f"Enseignant cree: {enseignant.nom}")
    else:
        print(f"Enseignant existe deja: {enseignant.nom}")

# 3. Créer des groupes (timetable)
from timetable.models import Groupe
groupes_data = [
    {"nom": "2A", "niveau": "2ème année", "effectif": 28},
    {"nom": "3B", "niveau": "3ème année", "effectif": 25},
    {"nom": "1C", "niveau": "1ère année", "effectif": 32},
    {"nom": "4D", "niveau": "4ème année", "effectif": 22},
]

for groupe_data in groupes_data:
    groupe, created = Groupe.objects.get_or_create(nom=groupe_data["nom"], defaults=groupe_data)
    if created:
        print(f"Groupe cree: {groupe.nom}")
    else:
        print(f"Groupe existe deja: {groupe.nom}")

# 4. Créer un département (departements)
from departements.models import Department
dept, created = Department.objects.get_or_create(
    name="Informatique", 
    code="INF", 
    defaults={"description": "Département d'informatique et technologies"}
)
if created:
    print(f"Departement cree: {dept.name}")
else:
    print(f"Departement existe deja: {dept.name}")

# 5. Créer des matières (subjects)
from subjects.models import Subject
subjects_data = [
    {"nom": "Mathématiques", "code": "MAT", "description": "Cours de mathématiques", "credits": 3, "heures_semaine": 4, "type_matiere": "core"},
    {"nom": "Physique", "code": "PHY", "description": "Cours de physique", "credits": 3, "heures_semaine": 3, "type_matiere": "core"},
    {"nom": "Informatique", "code": "INF", "description": "Programmation", "credits": 4, "heures_semaine": 5, "type_matiere": "core"},
    {"nom": "Chimie", "code": "CHI", "description": "Chimie générale", "credits": 3, "heures_semaine": 3, "type_matiere": "core"},
]

for subject_data in subjects_data:
    subject, created = Subject.objects.get_or_create(
        nom=subject_data["nom"],
        departement=dept,
        defaults=subject_data
    )
    if created:
        print(f"Matiere creee: {subject.nom}")
        # Assigner des enseignants
        enseignants = Enseignant.objects.all()[:2]
        subject.enseignants.add(*enseignants)
        print(f"   {enseignants.count()} enseignants assignes")
    else:
        print(f"Matiere existe deja: {subject.nom}")

# 6. Créer des types d'examens (exams)
from exams.models import ExamType
exam_types_data = [
    {"name": "Examen Partiel", "code": "PART", "description": "Examen de mi-semestre", "default_duration": 120, "max_score": 20.00},
    {"name": "Examen Final", "code": "FINAL", "description": "Examen de fin de semestre", "default_duration": 180, "max_score": 40.00},
    {"name": "Rattrapage", "code": "RAT", "description": "Examen de rattrapage", "default_duration": 120, "max_score": 20.00},
    {"name": "Test Rapide", "code": "TEST", "description": "Test de courte durée", "default_duration": 60, "max_score": 10.00},
]

for exam_type_data in exam_types_data:
    exam_type, created = ExamType.objects.get_or_create(
        code=exam_type_data["code"],
        defaults=exam_type_data
    )
    if created:
        print(f"Type d'examen cree: {exam_type.name}")
    else:
        print(f"Type d'examen existe deja: {exam_type.name}")

# 7. Créer une session d'examen
from exams.models import ExamSession
from datetime import date, timedelta
session, created = ExamSession.objects.get_or_create(
    name="Session Printemps 2024",
    defaults={
        "description": "Session d'examens du semestre de printemps",
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=30),
        "academic_year": "2023-2024",
        "is_active": True
    }
)

if created:
    print(f"Session d'examen creee: {session.name}")
else:
    print(f"Session d'examen existe deja: {session.name}")

print("\nResume des donnees creees:")
print(f"Salles: {Salle.objects.count()}")
print(f"Enseignants: {Enseignant.objects.count()}")
print(f"Groupes: {Groupe.objects.count()}")
print(f"Departements: {Department.objects.count()}")
print(f"Matières: {Subject.objects.count()}")
print(f"Types d'examens: {ExamType.objects.count()}")
print(f"Sessions d'examens: {ExamSession.objects.count()}")

print("\nToutes les donnees sont maintenant disponibles!")
print("Vous pouvez creer des examens depuis l'interface.")
