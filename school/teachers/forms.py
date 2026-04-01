from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'employee_id', 'first_name', 'last_name', 'gender', 'date_of_birth',
            'phone', 'email', 'address', 'hire_date', 'specialization',
            'department', 'status', 'salary'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: EMP001'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom de l\'enseignant'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'enseignant'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de téléphone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adresse complète'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Mathématiques, Physique...'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Département'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if not employee_id:
            raise forms.ValidationError('Le matricule est obligatoire')
        
        # Check if employee_id already exists (excluding current instance for updates)
        queryset = Teacher.objects.filter(employee_id=employee_id)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError('Ce matricule existe déjà')
        
        return employee_id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('L\'email est obligatoire')
        
        # Check if email already exists (excluding current instance for updates)
        queryset = Teacher.objects.filter(email=email)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError('Cet email existe déjà')
        
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Le téléphone est obligatoire')
        return phone
