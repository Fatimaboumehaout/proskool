from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Teacher
from .forms import TeacherForm

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teachers.html', context)

@login_required
def add_teacher(request):
    if request.method == 'POST':
        # Créer manuellement l'enseignant depuis les données POST
        teacher = Teacher(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            employee_id=request.POST.get('teacher_id'),
            gender=request.POST.get('gender', 'M'),
            date_of_birth=request.POST.get('date_of_birth'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            hire_date=request.POST.get('joining_date'),
            specialization=request.POST.get('qualification', ''),
            department=request.POST.get('department', ''),
            address=request.POST.get('address', ''),
        )
        teacher.save()
        messages.success(request, 'Teacher added successfully!')
        return redirect('teachers:teacher_list')
    
    # Pour le formulaire GET, nous pourrions avoir besoin de départements
    context = {'departments': []}  # Ajouter la logique des départements si nécessaire
    return render(request, 'teachers/add-teacher.html', context)

@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, employee_id=teacher_id)
    
    if request.method == 'POST':
        # Mettre à jour manuellement l'enseignant
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.gender = request.POST.get('gender', 'M')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.email = request.POST.get('email')
        teacher.phone = request.POST.get('phone')
        teacher.hire_date = request.POST.get('joining_date')
        teacher.specialization = request.POST.get('qualification', '')
        teacher.department = request.POST.get('department', '')
        teacher.address = request.POST.get('address', '')
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teachers:teacher_list')
    
    context = {
        'teacher': teacher,
        'departments': []  # Ajouter la logique des départements si nécessaire
    }
    return render(request, 'teachers/edit-teacher.html', context)

@login_required
def view_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, employee_id=teacher_id)
    context = {'teacher': teacher}
    return render(request, 'teachers/teacher-detail.html', context)

@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, employee_id=teacher_id)
    
    if request.method == 'POST':
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        teacher.delete()
        messages.success(request, f'Teacher {teacher_name} deleted successfully!')
        return redirect('teachers:teacher_list')
    
    return redirect('teachers:teacher_list')
