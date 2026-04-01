# home_auth/views.py 
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import CustomUser 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')
    
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'Home/dashboard.html')

def signup_view(request): 
    if request.method == 'POST': 
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name'] 
        email = request.POST['email'] 
        password = request.POST['password'] 
        role = request.POST.get('role')  # student, teacher ou admin 
 
        # Créer l'utilisateur 
        user = CustomUser.objects.create_user( 
            username=email, 
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
        ) 
 
        # Assigner le rôle 
        if role == 'student': 
            user.is_student = True 
        elif role == 'teacher': 
            user.is_teacher = True 
        elif role == 'admin': 
            user.is_admin = True 
 
        user.save() 
        login(request, user) 
        messages.success(request, 'Signup successful!') 
        return redirect('index') 
    return render(request, 'authentication/register.html')