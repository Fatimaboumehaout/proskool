# Script pour créer des données de test pour l'application subjects
# Exécutez avec : python manage.py shell < create_subjects_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from subjects.models import Subject, SubjectGroup, SubjectPrerequisite
from departements.models import Department
from timetable.models import Enseignant, Groupe

print("Création de données de test pour l'application subjects...")

# Vérifier qu'il y a des départements
if not Department.objects.exists():
    print("⚠️  Aucun département trouvé. Créez d'abord des départements.")
    exit()

# Vérifier qu'il y a des enseignants
if not Enseignant.objects.exists():
    print("⚠️  Aucun enseignant trouvé. Créez d'abord des enseignants.")
    exit()

# Vérifier qu'il y a des groupes
if not Groupe.objects.exists():
    print("⚠️  Aucun groupe trouvé. Créez d'abord des groupes.")
    exit()

# Créer des matières
subjects_data = [
    {
        "nom": "Mathématiques",
        "code": "MAT",
        "description": "Cours de mathématiques fondamentales",
        "credits": 3,
        "heures_semaine": 4,
        "type_matiere": "core",
        "departement": Department.objects.first()
    },
    {
        "nom": "Physique",
        "code": "PHY",
        "description": "Cours de physique générale",
        "credits": 3,
        "heures_semaine": 3,
        "type_matiere": "core",
        "departement": Department.objects.first()
    },
    {
        "nom": "Informatique",
        "code": "INF",
        "description": "Introduction à la programmation",
        "credits": 4,
        "heures_semaine": 5,
        "type_matiere": "core",
        "departement": Department.objects.first()
    },
    {
        "nom": "Français",
        "code": "FRA",
        "description": "Littérature et grammaire française",
        "credits": 2,
        "heures_semaine": 3,
        "type_matiere": "core",
        "departement": Department.objects.first()
    },
    {
        "nom": "Anglais",
        "code": "ANG",
        "description": "English language and literature",
        "credits": 2,
        "heures_semaine": 2,
        "type_matiere": "core",
        "departement": Department.objects.first()
    },
]

for subject_data in subjects_data:
    subject, created = Subject.objects.get_or_create(
        nom=subject_data["nom"],
        departement=subject_data["departement"],
        defaults=subject_data
    )
    if created:
        print(f"✅ Matière créée: {subject.nom}")
        
        # Assigner des enseignants
        enseignants = Enseignant.objects.all()[:2]  # Prendre les 2 premiers enseignants
        subject.enseignants.add(*enseignants)
        print(f"   👨‍🏫 {enseignants.count()} enseignants assignés")
    else:
        print(f"ℹ️  Matière existe déjà: {subject.nom}")

print(f"\n🎉 Total matières créées: {Subject.objects.count()}")

# Créer des associations matière-groupe
if Subject.objects.exists() and Groupe.objects.exists():
    for groupe in Groupe.objects.all()[:3]:  # Prendre les 3 premiers groupes
        for subject in Subject.objects.all()[:3]:  # Prendre les 3 premières matières
            subject_group, created = SubjectGroup.objects.get_or_create(
                subject=subject,
                groupe=groupe,
                defaults={
                    'enseignant_principal': Enseignant.objects.first(),
                    'heures_specifiques': subject.heures_semaine,
                    'credits_specifiques': subject.credits
                }
            )
            if created:
                print(f"✅ Association créée: {subject.nom} - {groupe.nom}")

print(f"\n🔗 Total associations matière-groupe: {SubjectGroup.objects.count()}")

print("\n🚀 Données de test créées avec succès!")
print("URLs de test:")
print("- Dashboard: http://127.0.0.1:8000/subjects/")
print("- Liste: http://127.0.0.1:8000/subjects/subjects/")
print("- Admin: http://127.0.0.1:8000/admin/")
