from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Salle(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la salle")
    capacite = models.PositiveIntegerField(verbose_name="Capacité")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.capacite} places)"

class Enseignant(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de l'enseignant")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    specialite = models.CharField(max_length=100, blank=True, verbose_name="Spécialité")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Groupe(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du groupe")
    niveau = models.CharField(max_length=50, blank=True, verbose_name="Niveau")
    effectif = models.PositiveIntegerField(blank=True, null=True, verbose_name="Effectif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.niveau})"

JOURS_SEMAINE = [
    ('Lundi', 'Lundi'),
    ('Mardi', 'Mardi'),
    ('Mercredi', 'Mercredi'),
    ('Jeudi', 'Jeudi'),
    ('Vendredi', 'Vendredi'),
    ('Samedi', 'Samedi'),
    ('Dimanche', 'Dimanche'),
]

PLAGES_HORAIRE = [
    ('08:00-09:30', '08:00-09:30'),
    ('09:45-11:15', '09:45-11:15'),
    ('11:30-13:00', '11:30-13:00'),
    ('14:00-15:30', '14:00-15:30'),
    ('15:45-17:15', '15:45-17:15'),
    ('17:30-19:00', '17:30-19:00'),
]

class Cours(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du cours")
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, verbose_name="Enseignant")
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, verbose_name="Groupe")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, verbose_name="Salle")
    jour_semaine = models.CharField(max_length=10, choices=JOURS_SEMAINE, verbose_name="Jour de la semaine")
    plage_horaire = models.CharField(max_length=11, choices=PLAGES_HORAIRE, verbose_name="Plage horaire")
    couleur = models.CharField(max_length=7, default='#007bff', verbose_name="Couleur (hex)")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['jour_semaine', 'plage_horaire']
        unique_together = ['jour_semaine', 'plage_horaire', 'enseignant']
        unique_together = ['jour_semaine', 'plage_horaire', 'salle']

    def __str__(self):
        return f"{self.nom} - {self.groupe.nom} - {self.jour_semaine} {self.plage_horaire}"

    def clean(self):
        # Vérifier les conflits d'enseignant
        conflit_enseignant = Cours.objects.filter(
            enseignant=self.enseignant,
            jour_semaine=self.jour_semaine,
            plage_horaire=self.plage_horaire
        ).exclude(pk=self.pk)
        
        if conflit_enseignant.exists():
            raise ValidationError(f"L'enseignant {self.enseignant.nom} a déjà un cours à ce créneau")

        # Vérifier les conflits de salle
        conflit_salle = Cours.objects.filter(
            salle=self.salle,
            jour_semaine=self.jour_semaine,
            plage_horaire=self.plage_horaire
        ).exclude(pk=self.pk)
        
        if conflit_salle.exists():
            raise ValidationError(f"La salle {self.salle.nom} est déjà occupée à ce créneau")

        # Vérifier les conflits de groupe
        conflit_groupe = Cours.objects.filter(
            groupe=self.groupe,
            jour_semaine=self.jour_semaine,
            plage_horaire=self.plage_horaire
        ).exclude(pk=self.pk)
        
        if conflit_groupe.exists():
            raise ValidationError(f"Le groupe {self.groupe.nom} a déjà un cours à ce créneau")

    def get_heure_debut(self):
        return self.plage_horaire.split('-')[0]

    def get_heure_fin(self):
        return self.plage_horaire.split('-')[1]
