# Python PFM  preskool- Plateforme de Gestion Scolaire

Une application web complète de gestion scolaire développée avec Django, conçue pour administrer efficacement les aspects académiques et administratifs d'un établissement d'enseignement.

## 📋 Description

Python PFM (Python Platform for Management) est un système intégré de gestion scolaire qui offre des fonctionnalités complètes pour la gestion des étudiants, du personnel, des cours, des examens, et de l'emploi du temps. Cette plateforme s'adresse aux établissements scolaires de tous niveaux cherchant une solution moderne et efficace.

## ✨ Fonctionnalités Principales

### 👤 Gestion des Utilisateurs
- **Système d'authentification personnalisé** avec rôles multiples
- **Profils utilisateurs** : Administrateurs, Enseignants, Étudiants
- **Gestion sécurisée des accès** et permissions

### 🎓 Gestion Académique
- **Gestion des étudiants** : fiches complètes avec informations parentales
- **Gestion du personnel** : enseignants et personnel administratif
- **Gestion des départements** et matières
- **Suivi des inscriptions** et admissions

### 📚 Gestion des Cours et Emploi du Temps
- **Planification des cours** avec gestion des salles
- **Emploi du temps interactif** pour étudiants et enseignants
- **Gestion des groupes** et classes
- **Affectation des enseignants** aux matières

### 📝 Gestion des Examens
- **Planification des examens** avec types variés (partiel, final, rattrapage)
- **Gestion des résultats** et statistiques
- **Sessions d'examens** organisées
- **Calcul automatique** des moyennes et taux de réussite
- **Appréciations automatiques** (A, B, C, D, E, F)

### 🏖️ Gestion des Vacances
- **Calendrier des vacances** scolaires
- **Planification des congés** et périodes de repos
- **Intégration avec l'emploi du temps**

## 🛠️ Architecture Technique

### Structure du Projet
```
school/
├── authentication/      # Gestion de l'authentification
├── home_auth/          # Modèle utilisateur personnalisé
├── student/            # Gestion des étudiants
├── teachers/           # Gestion des enseignants
├── faculty/            # Gestion du personnel
├── subjects/           # Gestion des matières
├── timetable/          # Emploi du temps et salles
├── departements/       # Gestion des départements
├── exams/              # Gestion des examens et résultats
├── holidays/           # Gestion des vacances
├── templates/          # Templates HTML
├── static/             # Fichiers statiques
└── school/             # Configuration principale
```

### Technologies Utilisées
- **Backend** : Django 6.0.3
- **Base de données** : SQLite (développement)
- **Frontend** : Templates Django avec HTML/CSS/JavaScript
- **Authentification** : Système personnalisé Django

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le repository**
   ```bash
   git clone <repository-url>
   cd python_pfm
   ```

2. **Créer et activer l'environnement virtuel**
   ```bash
   python -m venv monenv
   source monenv/bin/activate  # Windows: monenv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install django
   pip install pillow  # Pour la gestion des images
   ```

4. **Configurer la base de données**
   ```bash
   cd school
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Démarrer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - URL principale : http://127.0.0.1:8000/
   - Administration : http://127.0.0.1:8000/admin/

## 📊 Modèles de Données

### Utilisateurs
- **CustomUser** : Extension du modèle Django avec rôles spécifiques
- **Rôles disponibles** : admin, teacher, student

### Entités Principales
- **Student** : Informations complètes, y compris données parentales
- **Parent** : Coordonnées parents (père/mère)
- **Teacher** : Informations professionnelles des enseignants
- **Subject** : Matières et programmes
- **Exam** : Planification complète des examens
- **ExamResult** : Résultats et statistiques
- **Holiday** : Gestion des périodes de vacances

## 🔧 Configuration Principale

### Fichiers de Configuration Clés
- `school/settings.py` : Configuration Django principale
- `school/urls.py` : Routage des URLs
- `authentication/urls.py` : URLs d'authentification

### Variables d'Environnement
- `SECRET_KEY` : Clé secrète Django
- `DEBUG` : Mode de débogage
- `DATABASES` : Configuration de la base de données

## 🎯 Utilisation

### Flux de Travail Typique

1. **Administration**
   - Créer les départements et matières
   - Enregistrer les enseignants et étudiants
   - Configurer l'emploi du temps

2. **Gestion des Examens**
   - Définir les types d'examens
   - Planifier les sessions d'examens
   - Saisir les résultats

3. **Suivi Académique**
   - Consulter les statistiques
   - Générer les rapports
   - Gérer les vacances scolaires

### Accès par Rôle
- **Administrateur** : Accès complet à toutes les fonctionnalités
- **Enseignant** : Gestion des cours, examens, résultats
- **Étudiant** : Consultation de l'emploi du temps et résultats

## 🔄 Développement

### Scripts Utilitaires
- `create_test_teacher.py` : Script de création d'enseignants de test
- `create_more_teachers.py` : Script de création multiple d'enseignants

### Tests
```bash
python manage.py test
```

### Migration de la Base de Données
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📈 Statistiques et Rapports

Le système offre des fonctionnalités statistiques complètes :
- **Taux de réussite** par examen
- **Moyennes** et distributions de notes
- **Statistiques de présence** aux examens
- **Rapports académiques** personnalisables

## 🔒 Sécurité

- **Authentification sécurisée** avec Django
- **Gestion des permissions** par rôle
- **Protection CSRF** activée
- **Validation des données** côté serveur

## 🚀 Déploiement

### Production
- Configurer `DEBUG = False`
- Utiliser PostgreSQL/MySQL pour la production
- Configurer les variables d'environnement
- Mettre en place un serveur WSGI (Gunicorn + Nginx)

## 🤝 Contribuer

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

**Développé avec ❤️ pour l'éducation**
