# Script pour vérifier les dépendances de l'application exams
# Exécutez avec : python manage.py shell < check_dependencies.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

print("🔍 Vérification des dépendances pour l'application exams...")

# Vérifier les types d'examens
from exams.models import ExamType
exam_types = ExamType.objects.count()
print(f"📝 Types d'examens: {exam_types}")

# Vérifier les matières
try:
    from subjects.models import Subject
    subjects = Subject.objects.count()
    print(f"📚 Matières: {subjects}")
except:
    print("❌ Erreur: L'application subjects n'est pas disponible")

# Vérifier les salles
try:
    from timetable.models import Salle
    salles = Salle.objects.count()
    print(f"🏢 Salles: {salles}")
except:
    print("❌ Erreur: L'application timetable n'est pas disponible")

# Vérifier les enseignants
try:
    from timetable.models import Enseignant
    enseignants = Enseignant.objects.count()
    print(f"👨‍🏫 Enseignants: {enseignants}")
except:
    print("❌ Erreur: L'application timetable n'est pas disponible")

# Vérifier les groupes
try:
    from timetable.models import Groupe
    groupes = Groupe.objects.count()
    print(f"👥 Groupes: {groupes}")
except:
    print("❌ Erreur: L'application timetable n'est pas disponible")

# Vérifier les étudiants
try:
    from student.models import Student
    students = Student.objects.count()
    print(f"🎓 Étudiants: {students}")
except:
    print("❌ Erreur: L'application student n'est pas disponible")

print("\n📋 Résumé:")
if exam_types == 0:
    print("⚠️  Créez des types d'examens avec: python manage.py shell < create_exams_data.py")
if subjects == 0:
    print("⚠️  Créez des matières avec: python manage.py shell < quick_test_data.py")
if salles == 0:
    print("⚠️  Créez des salles avec: python manage.py shell < create_test_data.py")
if enseignants == 0:
    print("⚠️  Créez des enseignants avec: python manage.py shell < create_test_data.py")
if groupes == 0:
    print("⚠️  Créez des groupes avec: python manage.py shell < create_test_data.py")

print("\n🚀 Commandes à exécuter dans l'ordre:")
print("1. python manage.py shell < create_test_data.py  (pour timetable)")
print("2. python manage.py shell < quick_test_data.py   (pour subjects)")
print("3. python manage.py shell < create_exams_data.py (pour exams)")
