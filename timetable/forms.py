from django import forms
from .models import Salle, Enseignant, Groupe, Cours, JOURS_SEMAINE, PLAGES_HORAIRE

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'capacite', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la salle'
            }),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Capacité',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description (optionnelle)'
            })
        }

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'email', 'telephone', 'specialite']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone (optionnel)'
            }),
            'specialite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Spécialité (optionnelle)'
            })
        }

class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['nom', 'niveau', 'effectif']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du groupe'
            }),
            'niveau': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Niveau (ex: 2ème année)'
            }),
            'effectif': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Effectif',
                'min': 1
            })
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['nom', 'enseignant', 'groupe', 'salle', 'jour_semaine', 'plage_horaire', 'couleur', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du cours'
            }),
            'enseignant': forms.Select(attrs={
                'class': 'form-control'
            }),
            'groupe': forms.Select(attrs={
                'class': 'form-control'
            }),
            'salle': forms.Select(attrs={
                'class': 'form-control'
            }),
            'jour_semaine': forms.Select(attrs={
                'class': 'form-control'
            }),
            'plage_horaire': forms.Select(attrs={
                'class': 'form-control'
            }),
            'couleur': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'placeholder': '#007bff'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description (optionnelle)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enseignant'].queryset = Enseignant.objects.all().order_by('nom')
        self.fields['groupe'].queryset = Groupe.objects.all().order_by('nom')
        self.fields['salle'].queryset = Salle.objects.all().order_by('nom')

class EmploiDuTempsForm(forms.Form):
    groupe = forms.ModelChoiceField(
        queryset=Groupe.objects.all().order_by('nom'),
        empty_label="Sélectionner un groupe",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
