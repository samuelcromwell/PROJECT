from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


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
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('aboutus')  
        
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'users/traineelogin.html', {'form': form})

   
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account has been created successfully')
            return redirect('home')        
    else:
         form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})