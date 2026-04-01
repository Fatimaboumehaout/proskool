from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import CustomUser

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('authentication:dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'authentication/login.html')

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        if role == 'admin':
            user.is_admin = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'student':
            user.is_student = True
            
        user.save()
        login(request, user)
        return redirect('authentication:dashboard')
    
    return render(request, 'authentication/register.html')

@csrf_protect
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            messages.success(request, "Password reset instructions have been sent to your email.")
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email address.")
        return redirect('authentication:login')
    
    return render(request, 'authentication/forgot-password.html')

@csrf_protect
def reset_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            messages.success(request, "Password has been reset successfully.")
            return redirect('authentication:login')
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'authentication/reset_password.html')

def logout_view(request):
    logout(request)
    return redirect('authentication:login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    return render(request, 'Home/index.html')

def admin_dashboard_view(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('authentication:login')
    return render(request, 'Home/index.html')