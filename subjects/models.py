from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from departements.models import Department

class Subject(models.Model):
    CODE_CHOICES = [
        ('INF', 'Informatique'),
        ('MAT', 'Mathématiques'),
        ('PHY', 'Physique'),
        ('CHI', 'Chimie'),
        ('BIO', 'Biologie'),
        ('FRA', 'Français'),
        ('ANG', 'Anglais'),
        ('ESP', 'Espagnol'),
        ('HIS', 'Histoire'),
        ('GEO', 'Géographie'),
        ('ECO', 'Économie'),
        ('DRT', 'Droit'),
        ('ART', 'Arts'),
        ('MUS', 'Musique'),
        ('EPS', 'Sport'),
        ('AUT', 'Autre'),
    ]

    TYPE_CHOICES = [
        ('core', 'Matière principale'),
        ('optional', 'Matière optionnelle'),
        ('specialization', 'Spécialisation'),
        ('workshop', 'Atelier'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom de la matière")
    code = models.CharField(max_length=3, choices=CODE_CHOICES, verbose_name="Code matière")
    code_unique = models.CharField(max_length=10, unique=True, verbose_name="Code unique")
    description = models.TextField(blank=True, verbose_name="Description")
    credits = models.PositiveIntegerField(default=1, verbose_name="Crédits")
    heures_semaine = models.PositiveIntegerField(default=1, verbose_name="Heures par semaine")
    type_matiere = models.CharField(max_length=20, choices=TYPE_CHOICES, default='core', verbose_name="Type de matière")
    
    # Relations
    departement = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Département")
    enseignants = models.ManyToManyField('timetable.Enseignant', blank=True, verbose_name="Enseignants")
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['code_unique', 'nom']
        unique_together = ['code', 'departement']

    def __str__(self):
        return f"{self.code_unique} - {self.nom}"

    def clean(self):
        super().clean()
        # Générer le code unique automatiquement
        if not self.code_unique and self.code and self.departement:
            dept_code = self.departement.name[:3].upper()
            subject_count = Subject.objects.filter(departement=self.departement, code=self.code).count()
            self.code_unique = f"{self.code}{dept_code}{subject_count + 1:02d}"

        # Validation des heures
        if self.heures_semaine < 1 or self.heures_semaine > 40:
            raise ValidationError("Le nombre d'heures par semaine doit être entre 1 et 40.")

        # Validation des crédits
        if self.credits < 1 or self.credits > 20:
            raise ValidationError("Le nombre de crédits doit être entre 1 et 20.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_total_heures(self):
        """Retourne le total d'heures pour cette matière"""
        return self.heures_semaine * self.credits

    def get_enseignants_count(self):
        """Retourne le nombre d'enseignants assignés"""
        return self.enseignants.count()

class SubjectGroup(models.Model):
    """Association matière-groupe pour la gestion des classes"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    groupe = models.ForeignKey('timetable.Groupe', on_delete=models.CASCADE, verbose_name="Groupe")
    enseignant_principal = models.ForeignKey('timetable.Enseignant', on_delete=models.SET_NULL, null=True, verbose_name="Enseignant principal")
    
    # Paramètres spécifiques au groupe
    heures_specifiques = models.PositiveIntegerField(null=True, blank=True, verbose_name="Heures spécifiques (si différent)")
    credits_specifiques = models.PositiveIntegerField(null=True, blank=True, verbose_name="Crédits spécifiques (si différent)")
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Matière par groupe"
        verbose_name_plural = "Matières par groupe"
        unique_together = ['subject', 'groupe']
        ordering = ['subject', 'groupe']

    def __str__(self):
        return f"{self.subject.nom} - {self.groupe.nom}"

    def get_heures_effectives(self):
        """Retourne le nombre d'heures effectives pour ce groupe"""
        return self.heures_specifiques or self.subject.heures_semaine

    def get_credits_effectifs(self):
        """Retourne le nombre de crédits effectifs pour ce groupe"""
        return self.credits_specifiques or self.subject.credits

class SubjectPrerequisite(models.Model):
    """Prérequis entre matières"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='prerequis_for', verbose_name="Matière requise")
    prerequisite = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='prerequisite_for', verbose_name="Prérequis")
    niveau_requis = models.CharField(max_length=50, blank=True, verbose_name="Niveau requis")
    description = models.TextField(blank=True, verbose_name="Description du prérequis")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Prérequis de matière"
        verbose_name_plural = "Prérequis de matières"
        unique_together = ['subject', 'prerequisite']

    def __str__(self):
        return f"{self.prerequisite.nom} → {self.subject.nom}"

    def clean(self):
        super().clean()
        if self.subject == self.prerequisite:
            raise ValidationError("Une matière ne peut pas être son propre prérequis.")
