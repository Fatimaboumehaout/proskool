# Script simple pour vérifier les dépendances (sans emojis)
# Exécutez avec : python manage.py shell < check_simple.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

print("Verification des dependances pour l'application exams...")

# Vérifier les types d'examens
from exams.models import ExamType
exam_types = ExamType.objects.count()
print(f"Types d'examens: {exam_types}")

# Vérifier les matières
try:
    from subjects.models import Subject
    subjects = Subject.objects.count()
    print(f"Matières: {subjects}")
except:
    print("Erreur: L'application subjects n'est pas disponible")

# Vérifier les salles
try:
    from timetable.models import Salle
    salles = Salle.objects.count()
    print(f"Salles: {salles}")
except:
    print("Erreur: L'application timetable n'est pas disponible")

# Vérifier les enseignants
try:
    from timetable.models import Enseignant
    enseignants = Enseignant.objects.count()
    print(f"Enseignants: {enseignants}")
except:
    print("Erreur: L'application timetable n'est pas disponible")

# Vérifier les groupes
try:
    from timetable.models import Groupe
    groupes = Groupe.objects.count()
    print(f"Groupes: {groupes}")
except:
    print("Erreur: L'application timetable n'est pas disponible")

print("\nResume:")
if exam_types == 0:
    print("ATTENTION: Crenez des types d'examens")
if subjects == 0:
    print("ATTENTION: Crenez des matieres")
if salles == 0:
    print("ATTENTION: Crenez des salles")
if enseignants == 0:
    print("ATTENTION: Crenez des enseignants")
if groupes == 0:
    print("ATTENTION: Crenez des groupes")

print("\nCommandes a executer dans l'ordre:")
print("1. python manage.py shell < create_test_data.py")
print("2. python manage.py shell < quick_test_data.py")
print("3. python manage.py shell < create_exams_data.py")
