#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from teachers.models import Teacher
from django.contrib.auth import get_user_model

User = get_user_model()

# Créer un enseignant test
if not Teacher.objects.exists():
    user = User.objects.create_user(
        username='teacher1',
        email='teacher1@example.com',
        password='password123',
        first_name='John',
        last_name='Doe'
    )
    
    teacher = Teacher.objects.create(
        user=user,
        employee_id='EMP001',
        first_name='John',
        last_name='Doe',
        gender='M',
        date_of_birth='1980-01-01',
        phone='0612345678',
        email='teacher1@example.com',
        address='123 Test Street',
        hire_date='2020-01-01',
        specialization='Mathematics',
        department='Science',
        status='active',
        salary=50000.00
    )
    print('Teacher created successfully!')
    print('Username: teacher1, Password: password123')
else:
    print('Teachers already exist:', Teacher.objects.count())
    for teacher in Teacher.objects.all():
        print(f'- {teacher.employee_id}: {teacher.first_name} {teacher.last_name}')
