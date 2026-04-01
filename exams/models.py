from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Avg, Max, Min, Count
from datetime import datetime, timedelta

class ExamType(models.Model):
    """Types d'examens (partiel, final, rattrapage, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Nom du type")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    default_duration = models.PositiveIntegerField(default=120, verbose_name="Durée par défaut (minutes)")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, verbose_name="Note maximale")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Type d'examen"
        verbose_name_plural = "Types d'examens"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.max_score} pts)"

class Exam(models.Model):
    """Planification des examens"""
    STATUS_CHOICES = [
        ('planned', 'Planifié'),
        ('ongoing', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre de l'examen")
    description = models.TextField(blank=True, verbose_name="Description")
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, verbose_name="Type d'examen")
    
    # Relations
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, verbose_name="Matière")
    groups = models.ManyToManyField('timetable.Groupe', verbose_name="Groupes")
    teachers = models.ManyToManyField('timetable.Enseignant', verbose_name="Surveillants")
    room = models.ForeignKey('timetable.Salle', on_delete=models.CASCADE, verbose_name="Salle")
    
    # Planification
    exam_date = models.DateField(verbose_name="Date de l'examen")
    start_time = models.TimeField(verbose_name="Heure de début")
    duration = models.PositiveIntegerField(verbose_name="Durée (minutes)")
    end_time = models.TimeField(verbose_name="Heure de fin", blank=True, null=True)
    
    # Paramètres
    max_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Note maximale")
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Note de passage")
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name="Statut")
    is_published = models.BooleanField(default=False, verbose_name="Publié")
    
    # Métadonnées
    created_by = models.ForeignKey('authentication.CustomUser', on_delete=models.SET_NULL, null=True, verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Examens"
        ordering = ['-exam_date', '-start_time']

    def __str__(self):
        return f"{self.title} - {self.exam_date}"

    def clean(self):
        super().clean()
        
        # Calculer l'heure de fin
        if self.start_time and self.duration:
            start_datetime = datetime.combine(datetime.today(), self.start_time)
            end_datetime = start_datetime + timedelta(minutes=self.duration)
            self.end_time = end_datetime.time()
        
        # Valider que la note de passage <= note maximale
        if self.passing_score and self.max_score:
            if self.passing_score > self.max_score:
                raise ValidationError("La note de passage ne peut pas être supérieure à la note maximale.")
        
        # Valider la durée
        if self.duration and (self.duration < 15 or self.duration > 480):
            raise ValidationError("La durée doit être entre 15 minutes et 8 heures.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_total_students(self):
        """Retourne le nombre total d'étudiants concernés"""
        from student.models import Student
        return Student.objects.filter(group__in=self.groups.all()).count()

    def get_submitted_count(self):
        """Retourne le nombre de copies soumises"""
        return self.results.filter(status='submitted').count()

    def get_average_score(self):
        """Retourne la moyenne des notes"""
        avg = self.results.filter(status='graded').aggregate(avg=Avg('score'))['avg']
        return round(avg, 2) if avg else 0

    def get_success_rate(self):
        """Retourne le taux de réussite"""
        total_graded = self.results.filter(status='graded').count()
        if total_graded == 0:
            return 0
        passed = self.results.filter(status='graded', score__gte=self.passing_score).count()
        return round((passed / total_graded) * 100, 1)

class ExamResult(models.Model):
    """Résultats des examens par étudiant"""
    STATUS_CHOICES = [
        ('absent', 'Absent'),
        ('submitted', 'Soumis'),
        ('graded', 'Noté'),
        ('appealed', 'Contesté'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', verbose_name="Examen")
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, verbose_name="Étudiant")
    
    # Notes
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Note")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Note maximale")
    
    # Appréciation
    comment = models.TextField(blank=True, verbose_name="Commentaire")
    grade = models.CharField(max_length=5, blank=True, verbose_name="Appréciation (A, B, C, etc.)")
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', verbose_name="Statut")
    is_passed = models.BooleanField(null=True, blank=True, verbose_name="Admis")
    
    # Dates
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de soumission")
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de notation")
    graded_by = models.ForeignKey('authentication.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Noté par")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Résultat d'examen"
        verbose_name_plural = "Résultats d'examens"
        unique_together = ['exam', 'student']
        ordering = ['-exam__exam_date', 'student__last_name']

    def __str__(self):
        return f"{self.student} - {self.exam.title}"

    def clean(self):
        super().clean()
        
        # Valider la note
        if self.score is not None:
            if self.score < 0 or self.score > self.max_score:
                raise ValidationError(f"La note doit être entre 0 et {self.max_score}.")
            
            # Déterminer si l'étudiant est admis
            if self.exam:
                self.is_passed = self.score >= self.exam.passing_score

    def save(self, *args, **kwargs):
        self.clean()
        
        # Mettre à jour les dates automatiquement
        if self.status == 'submitted' and not self.submitted_at:
            self.submitted_at = timezone.now()
        
        if self.status == 'graded' and not self.graded_at:
            self.graded_at = timezone.now()
        
        # Calculer l'appréciation automatiquement
        if self.score is not None and self.max_score > 0:
            percentage = (self.score / self.max_score) * 100
            self.grade = self.calculate_grade(percentage)
        
        super().save(*args, **kwargs)

    def calculate_grade(self, percentage):
        """Calcule l'appréciation en fonction du pourcentage"""
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        elif percentage >= 50:
            return 'E'
        else:
            return 'F'

    def get_percentage(self):
        """Retourne le pourcentage de la note"""
        if self.score is not None and self.max_score > 0:
            return round((self.score / self.max_score) * 100, 1)
        return 0

class ExamSession(models.Model):
    """Session d'examen (période d'examens)"""
    name = models.CharField(max_length=100, verbose_name="Nom de la session")
    description = models.TextField(blank=True, verbose_name="Description")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    academic_year = models.CharField(max_length=20, verbose_name="Année académique")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Session d'examen"
        verbose_name_plural = "Sessions d'examens"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

    def get_exams_count(self):
        """Retourne le nombre d'examens dans cette session"""
        return Exam.objects.filter(
            exam_date__gte=self.start_date,
            exam_date__lte=self.end_date
        ).count()

    def get_total_students(self):
        """Retourne le nombre total d'étudiants concernés"""
        from student.models import Student
        return Student.objects.filter(group__exam__exam_date__gte=self.start_date,
                                   group__exam__exam_date__lte=self.end_date).distinct().count()

class ExamStatistics(models.Model):
    """Statistiques des examens"""
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, verbose_name="Examen")
    
    # Statistiques de base
    total_students = models.PositiveIntegerField(default=0, verbose_name="Total étudiants")
    submitted_count = models.PositiveIntegerField(default=0, verbose_name="Copies soumises")
    graded_count = models.PositiveIntegerField(default=0, verbose_name="Copies notées")
    absent_count = models.PositiveIntegerField(default=0, verbose_name="Absents")
    
    # Statistiques de notes
    average_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Moyenne")
    highest_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Note la plus haute")
    lowest_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Note la plus basse")
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Taux de réussite (%)")
    
    # Distribution des notes
    a_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de A")
    b_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de B")
    c_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de C")
    d_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de D")
    e_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de E")
    f_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de F")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Statistiques d'examen"
        verbose_name_plural = "Statistiques d'examens"

    def __str__(self):
        return f"Stats - {self.exam.title}"

    def update_statistics(self):
        """Met à jour les statistiques"""
        results = self.exam.results.all()
        
        # Comptages
        self.total_students = self.exam.get_total_students()
        self.submitted_count = results.filter(status='submitted').count()
        self.graded_count = results.filter(status='graded').count()
        self.absent_count = results.filter(status='absent').count()
        
        # Statistiques de notes
        graded_results = results.filter(status='graded', score__isnull=False)
        if graded_results.exists():
            scores = [r.score for r in graded_results]
            self.average_score = sum(scores) / len(scores)
            self.highest_score = max(scores)
            self.lowest_score = min(scores)
            self.success_rate = self.exam.get_success_rate()
        
        # Distribution des appréciations
        self.a_count = graded_results.filter(grade='A').count()
        self.b_count = graded_results.filter(grade='B').count()
        self.c_count = graded_results.filter(grade='C').count()
        self.d_count = graded_results.filter(grade='D').count()
        self.e_count = graded_results.filter(grade='E').count()
        self.f_count = graded_results.filter(grade='F').count()
        
        self.save()
