# Script pour créer des données de test pour l'application exams
# Exécutez avec : python manage.py shell < create_exams_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from exams.models import ExamType, ExamSession
from subjects.models import Subject
from timetable.models import Enseignant, Groupe, Salle
from datetime import date, timedelta

print("🚀 Création de données de test pour l'application exams...")

# Créer des types d'examens
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
        print(f"✅ Type d'examen créé: {exam_type.name}")
    else:
        print(f"ℹ️  Type d'examen existe déjà: {exam_type.name}")

# Créer une session d'examen
session, created = ExamSession.objects.get_or_create(
    name="Session d'examens Printemps 2024",
    defaults={
        "description": "Session d'examens du semestre de printemps",
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=30),
        "academic_year": "2023-2024",
        "is_active": True
    }
)

if created:
    print(f"✅ Session d'examen créée: {session.name}")
else:
    print(f"ℹ️  Session d'examen existe déjà: {session.name}")

# Vérifier les données existantes
print(f"\n📊 Résumé des données créées:")
print(f"📝 Types d'examens: {ExamType.objects.count()}")
print(f"📅 Sessions d'examens: {ExamSession.objects.count()}")

# Vérifier les dépendances
print(f"\n🔗 Dépendances:")
print(f"📚 Matières: {Subject.objects.count()}")
print(f"👨‍🏫 Enseignants: {Enseignant.objects.count()}")
print(f"👥 Groupes: {Groupe.objects.count()}")
print(f"🏢 Salles: {Salle.objects.count()}")

if Subject.objects.exists() and Enseignant.objects.exists() and Groupe.objects.exists() and Salle.objects.exists():
    print("\n🎉 Toutes les dépendances sont prêtes!")
    print("Vous pouvez maintenant créer des examens depuis l'interface.")
else:
    print("\n⚠️  Certaines dépendances manquent:")
    if not Subject.objects.exists():
        print("   - Créez d'abord des matières (subjects)")
    if not Enseignant.objects.exists():
        print("   - Créez d'abord des enseignants (timetable)")
    if not Groupe.objects.exists():
        print("   - Créez d'abord des groupes (timetable)")
    if not Salle.objects.exists():
        print("   - Créez d'abord des salles (timetable)")

print("\n🚀 Données de test créées avec succès!")
print("URLs de test:")
print("- Dashboard: http://127.0.0.1:8000/exams/")
print("- Admin: http://127.0.0.1:8000/admin/")
