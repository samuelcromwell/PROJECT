from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as auth_login # library for user authentication

def home(request):
    return render(request, 'users/home.html')
def admin(request):
    return render(request, 'users/admin.html')
def aboutus(request):
    return render(request, 'users/aboutus.html')
def login(request):
    return render(request, 'users/login.html')
def courses(request):
    return render(request, 'users/courses.html')

def traineelogin(request):
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        user = authenticate(request, username = username, password = password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Login successful.')
            return redirect('/')  
    
        else:
            messages.error(request, f'Invalid username or password.')
    
        messages.error(request, f'Fill in the form correctly.')
   
    return render(request, 'users/traineelogin.html') 

   
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account has been created successfully, kindly login with your username and password')
            return redirect('home')        
    else:
         form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})