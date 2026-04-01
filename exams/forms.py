from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Exam, ExamResult, ExamSession, ExamType

class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'code', 'description', 'default_duration', 'max_score', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 10}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'default_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'max': 480}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100, 'step': 0.01}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_default_duration(self):
        duration = self.cleaned_data.get('default_duration')
        if duration and (duration < 15 or duration > 480):
            raise ValidationError("La durée doit être entre 15 et 480 minutes.")
        return duration

    def clean_max_score(self):
        score = self.cleaned_data.get('max_score')
        if score and (score < 1 or score > 100):
            raise ValidationError("La note maximale doit être entre 1 et 100.")
        return score

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'title', 'description', 'exam_type', 'subject', 'groups', 'teachers', 'room',
            'exam_date', 'start_time', 'duration', 'max_score', 'passing_score', 
            'status', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 4}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 4}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'max': 480}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100, 'step': 0.01}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': 0.01}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les enseignants et salles
        self.fields['teachers'].queryset = self.fields['teachers'].queryset.order_by('nom')
        self.fields['room'].queryset = self.fields['room'].queryset.order_by('nom')

    def clean(self):
        cleaned_data = super().clean()
        exam_date = cleaned_data.get('exam_date')
        start_time = cleaned_data.get('start_time')
        duration = cleaned_data.get('duration')
        room = cleaned_data.get('room')
        groups = cleaned_data.get('groups')
        teachers = cleaned_data.get('teachers')
        max_score = cleaned_data.get('max_score')
        passing_score = cleaned_data.get('passing_score')

        # Validation des dates et heures
        if exam_date and start_time and duration:
            exam_datetime = timezone.make_aware(datetime.combine(exam_date, start_time))
            if exam_datetime < timezone.now():
                raise ValidationError("L'examen ne peut pas être planifié dans le passé.")

        # Validation de la note de passage
        if max_score and passing_score:
            if passing_score > max_score:
                raise ValidationError("La note de passage ne peut pas être supérieure à la note maximale.")

        # Validation de la durée
        if duration and (duration < 15 or duration > 480):
            raise ValidationError("La durée doit être entre 15 minutes et 8 heures.")

        # Validation des conflits de salle
        if exam_date and start_time and duration and room:
            end_time = (datetime.combine(exam_date, start_time) + timedelta(minutes=duration)).time()
            
            # Vérifier les conflits avec d'autres examens
            conflicting_exams = Exam.objects.filter(
                room=room,
                exam_date=exam_date,
                status__in=['planned', 'ongoing']
            ).exclude(pk=self.instance.pk if self.instance.pk else None)

            for exam in conflicting_exams:
                # Vérifier le chevauchement des horaires
                if (start_time < exam.end_time and end_time > exam.start_time):
                    raise ValidationError(f"Conflit de salle avec l'examen '{exam.title}' prévu dans la même salle.")

        # Validation des conflits d'enseignants
        if exam_date and start_time and duration and teachers:
            end_time = (datetime.combine(exam_date, start_time) + timedelta(minutes=duration)).time()
            
            for teacher in teachers:
                conflicting_exams = Exam.objects.filter(
                    teachers=teacher,
                    exam_date=exam_date,
                    status__in=['planned', 'ongoing']
                ).exclude(pk=self.instance.pk if self.instance.pk else None)

                for exam in conflicting_exams:
                    if (start_time < exam.end_time and end_time > exam.start_time):
                        raise ValidationError(f"Conflit de surveillance pour l'enseignant '{teacher}' avec l'examen '{exam.title}'.")

        return cleaned_data

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['exam', 'student', 'score', 'max_score', 'comment', 'status', 'is_passed']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': 0.01}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100, 'step': 0.01}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_passed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les étudiants par groupe si un examen est sélectionné
        if 'exam' in self.data:
            try:
                exam_id = int(self.data.get('exam'))
                exam = Exam.objects.get(pk=exam_id)
                self.fields['student'].queryset = exam.get_all_students().order_by('last_name')
                self.fields['max_score'].initial = exam.max_score
            except (ValueError, Exam.DoesNotExist):
                self.fields['student'].queryset = []
        elif self.instance.pk and self.instance.exam:
            exam = self.instance.exam
            self.fields['student'].queryset = exam.get_all_students().order_by('last_name')
        else:
            self.fields['student'].queryset = []

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        max_score = cleaned_data.get('max_score')
        status = cleaned_data.get('status')

        # Validation de la note
        if score is not None and max_score:
            if score < 0 or score > max_score:
                raise ValidationError(f"La note doit être entre 0 et {max_score}.")

        # Validation du statut
        if status == 'graded' and score is None:
            raise ValidationError("Une note est requise pour marquer le résultat comme noté.")

        if status == 'absent' and score is not None:
            raise ValidationError("Un étudiant absent ne peut pas avoir de note.")

        return cleaned_data

class ExamSessionForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        fields = ['name', 'description', 'start_date', 'end_date', 'academic_year', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2023-2024'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("La date de début doit être antérieure à la date de fin.")

        return cleaned_data

class BulkGradingForm(forms.Form):
    """Formulaire pour la notation en masse"""
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.filter(status__in=['ongoing', 'completed']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Examen"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter dynamiquement les champs de notes pour chaque étudiant
        exam_id = kwargs.get('data', {}).get('exam')
        if exam_id:
            try:
                exam = Exam.objects.get(pk=exam_id)
                students = exam.get_all_students()
                for student in students:
                    field_name = f'score_{student.id}'
                    self.fields[field_name] = forms.DecimalField(
                        required=False,
                        min_value=0,
                        max_value=exam.max_score,
                        decimal_places=2,
                        widget=forms.NumberInput(attrs={
                            'class': 'form-control',
                            'placeholder': f'Max: {exam.max_score}'
                        }),
                        label=f"{student.first_name} {student.last_name}"
                    )
            except Exam.DoesNotExist:
                pass
