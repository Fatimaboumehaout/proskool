# Script pour créer des données de test pour l'emploi du temps
# Exécutez avec : python manage.py shell < create_test_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from timetable.models import Salle, Enseignant, Groupe, Cours

print("Création des données de test...")

# Créer des salles
salles_data = [
    {"nom": "Salle A101", "capacite": 30, "description": "Salle de cours principale"},
    {"nom": "Salle B205", "capacite": 25, "description": "Salle informatique"},
    {"nom": "Salle C150", "capacite": 40, "description": "Amphithéâtre"},
    {"nom": "Labo Chimie", "capacite": 20, "description": "Laboratoire de chimie"},
]

for salle_data in salles_data:
    salle, created = Salle.objects.get_or_create(nom=salle_data["nom"], defaults=salle_data)
    if created:
        print(f"✅ Salle créée: {salle.nom}")
    else:
        print(f"ℹ️  Salle existe déjà: {salle.nom}")

# Créer des enseignants
enseignants_data = [
    {"nom": "Dupont Jean", "email": "dupont@ecole.fr", "telephone": "0123456789", "specialite": "Mathématiques"},
    {"nom": "Marie Sophie", "email": "marie@ecole.fr", "telephone": "0234567890", "specialite": "Physique"},
    {"nom": "Martin Paul", "email": "martin@ecole.fr", "telephone": "0345678901", "specialite": "Informatique"},
    {"nom": "Durand Claire", "email": "durand@ecole.fr", "telephone": "0456789012", "specialite": "Chimie"},
]

for enseignant_data in enseignants_data:
    enseignant, created = Enseignant.objects.get_or_create(email=enseignant_data["email"], defaults=enseignant_data)
    if created:
        print(f"✅ Enseignant créé: {enseignant.nom}")
    else:
        print(f"ℹ️  Enseignant existe déjà: {enseignant.nom}")

# Créer des groupes
groupes_data = [
    {"nom": "2A", "niveau": "2ème année", "effectif": 28},
    {"nom": "3B", "niveau": "3ème année", "effectif": 25},
    {"nom": "1C", "niveau": "1ère année", "effectif": 32},
    {"nom": "4D", "niveau": "4ème année", "effectif": 22},
]

for groupe_data in groupes_data:
    groupe, created = Groupe.objects.get_or_create(nom=groupe_data["nom"], defaults=groupe_data)
    if created:
        print(f"✅ Groupe créé: {groupe.nom}")
    else:
        print(f"ℹ️  Groupe existe déjà: {groupe.nom}")

print("\n🎉 Données de test créées avec succès!")
print(f"Salles: {Salle.objects.count()}")
print(f"Enseignants: {Enseignant.objects.count()}")
print(f"Groupes: {Groupe.objects.count()}")

# Créer quelques cours d'exemple
cours_data = [
    {
        "nom": "Mathématiques",
        "enseignant": Enseignant.objects.get(nom="Dupont Jean"),
        "groupe": Groupe.objects.get(nom="2A"),
        "salle": Salle.objects.get(nom="Salle A101"),
        "jour_semaine": "Lundi",
        "plage_horaire": "08:00-09:30",
        "couleur": "#007bff",
        "description": "Cours de mathématiques avancées"
    },
    {
        "nom": "Physique",
        "enseignant": Enseignant.objects.get(nom="Marie Sophie"),
        "groupe": Groupe.objects.get(nom="2A"),
        "salle": Salle.objects.get(nom="Labo Chimie"),
        "jour_semaine": "Lundi",
        "plage_horaire": "09:45-11:15",
        "couleur": "#28a745",
        "description": "Cours de physique expérimentale"
    },
    {
        "nom": "Informatique",
        "enseignant": Enseignant.objects.get(nom="Martin Paul"),
        "groupe": Groupe.objects.get(nom="3B"),
        "salle": Salle.objects.get(nom="Salle B205"),
        "jour_semaine": "Mardi",
        "plage_horaire": "10:00-11:30",
        "couleur": "#ffc107",
        "description": "Programmation Python"
    },
]

for cours_data in cours_data:
    cours, created = Cours.objects.get_or_create(
        nom=cours_data["nom"],
        groupe=cours_data["groupe"],
        jour_semaine=cours_data["jour_semaine"],
        plage_horaire=cours_data["plage_horaire"],
        defaults=cours_data
    )
    if created:
        print(f"✅ Cours créé: {cours.nom}")
    else:
        print(f"ℹ️  Cours existe déjà: {cours.nom}")

print(f"\n📚 Total cours créés: {Cours.objects.count()}")
print("\n🚀 Vous pouvez maintenant tester l'application!")
print("URL: http://127.0.0.1:8000/timetable/emploi-du-temps/")
