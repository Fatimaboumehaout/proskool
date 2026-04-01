from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Parent
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='authentication:login')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/students.html', {'students': students})

@login_required(login_url='authentication:login')
def add_student(request):
    if request.method == 'POST':
        # Student data
        sid = request.POST.get('student_id')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        sclass = request.POST.get('student_class')
        dob = request.POST.get('date_of_birth')
        mobile = request.POST.get('mobile_number')
        admission = request.POST.get('admission_number')
        section = request.POST.get('section')
        gender = request.POST.get('gender')
        joining = request.POST.get('joining_date')
        image = request.FILES.get('student_image')
        
        # Parent data
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        
        # Create parent first
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )
        
        # Create student with parent relationship
        Student.objects.create(
            student_id=sid,
            first_name=fname,
            last_name=lname,
            student_class=sclass,
            date_of_birth=dob,
            mobile_number=mobile,
            admission_number=admission,
            section=section,
            gender=gender,
            joining_date=joining,
            student_image=image,
            parent=parent
        )
        # Afficher message et rediriger vers la liste
        messages.success(request, 'Student added Successfully')
        return redirect('student:student_list')
    return render(request, 'students/add-student.html')

@login_required(login_url='authentication:login')
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_class = request.POST.get('student_class')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        student.gender = request.POST.get('gender')
        student.joining_date = request.POST.get('joining_date')
        
        image = request.FILES.get('student_image')
        if image:
            student.student_image = image
            
        student.save()
        return redirect('student:student_list')
    return render(request, 'students/edit-student.html', {'student': student})

@login_required(login_url='authentication:login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.delete()
    return redirect('student:student_list')

@login_required(login_url='authentication:login')
def student_details(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student})