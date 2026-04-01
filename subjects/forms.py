from django import forms
from django.core.exceptions import ValidationError
from .models import Subject, SubjectGroup, SubjectPrerequisite

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['nom', 'code', 'description', 'credits', 'heures_semaine', 'type_matiere', 'departement', 'enseignants', 'is_active']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la matière'
            }),
            'code': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la matière'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20,
                'placeholder': 'Crédits'
            }),
            'heures_semaine': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 40,
                'placeholder': 'Heures par semaine'
            }),
            'type_matiere': forms.Select(attrs={
                'class': 'form-control'
            }),
            'departement': forms.Select(attrs={
                'class': 'form-control'
            }),
            'enseignants': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 4
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enseignants'].queryset = self.fields['enseignants'].queryset.order_by('nom')

    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits and (credits < 1 or credits > 20):
            raise ValidationError("Le nombre de crédits doit être entre 1 et 20.")
        return credits

    def clean_heures_semaine(self):
        heures = self.cleaned_data.get('heures_semaine')
        if heures and (heures < 1 or heures > 40):
            raise ValidationError("Le nombre d'heures par semaine doit être entre 1 et 40.")
        return heures

class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = ['subject', 'groupe', 'enseignant_principal', 'heures_specifiques', 'credits_specifiques', 'is_active']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
            'groupe': forms.Select(attrs={
                'class': 'form-control'
            }),
            'enseignant_principal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'heures_specifiques': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 40,
                'placeholder': 'Optionnel'
            }),
            'credits_specifiques': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20,
                'placeholder': 'Optionnel'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enseignant_principal'].queryset = self.fields['enseignant_principal'].queryset.order_by('nom')

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        groupe = cleaned_data.get('groupe')
        
        # Vérifier que cette association n'existe pas déjà
        if subject and groupe:
            existing = SubjectGroup.objects.filter(subject=subject, groupe=groupe)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError("Cette matière est déjà associée à ce groupe.")

        return cleaned_data

class SubjectPrerequisiteForm(forms.ModelForm):
    class Meta:
        model = SubjectPrerequisite
        fields = ['subject', 'prerequisite', 'niveau_requis', 'description']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
            'prerequisite': forms.Select(attrs={
                'class': 'form-control'
            }),
            'niveau_requis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2ème année'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du prérequis'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        prerequisite = cleaned_data.get('prerequisite')
        
        if subject and prerequisite:
            if subject == prerequisite:
                raise ValidationError("Une matière ne peut pas être son propre prérequis.")
            
            # Vérifier que ce prérequis n'existe pas déjà
            existing = SubjectPrerequisite.objects.filter(subject=subject, prerequisite=prerequisite)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError("Ce prérequis existe déjà.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les matières par département si nécessaire
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['prerequisite'].queryset = Subject.objects.filter(
                    departement_id=Subject.objects.get(pk=subject_id).departement_id
                ).exclude(pk=subject_id)
            except (ValueError, Subject.DoesNotExist):
                self.fields['prerequisite'].queryset = Subject.objects.none()
        elif self.instance.pk and self.instance.subject:
            self.fields['prerequisite'].queryset = Subject.objects.filter(
                departement=self.instance.subject.departement
            ).exclude(pk=self.instance.subject.pk)
        else:
            self.fields['prerequisite'].queryset = Subject.objects.none()
