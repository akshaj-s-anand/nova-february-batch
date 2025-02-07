from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('sample')
        
            else:
                messages.error(request, f"Sorry {username}, you do not have permission to access this page.")
        else:
            messages.error(request, 'Invalid username or password')    
            
        
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect("login")