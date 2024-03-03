from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as auth_login # library for user authentication
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'users/home.html')
def aboutus(request):
    return render(request, 'users/aboutus.html')
def login(request):
    return render(request, 'users/login.html')
def courses(request):
    return render(request, 'users/courses.html')
def truck(request):
    return render(request, 'users/truck.html')
def car(request):
    return render(request, 'users/car.html')

def traineelogin(request):
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = authenticate(request, username = username, password = password)

        if user is not None:
             # Check if the user belongs to the 'trainee' group
            trainee_group = Group.objects.get(name='trainee')
            if trainee_group in user.groups.all():
                auth_login(request, user)
                # messages.success(request, f'Login successful.')
                return redirect('base')  
            else:
                messages.error(request, f'Sorry, you are not authorized to login as a Trainee.')
                return redirect('login')
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
            messages.success(request, f'Hi {username}, your account has been created successfully, you will be able to login with your new username and password once your registration has been approved')
            return redirect('login')        
    else:
         form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})

def instructorlogin(request):
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = authenticate(request, username = username, password = password)

        if user is not None:
             # Check if the user belongs to the 'instructor' group
            instructor_group = Group.objects.get(name='instructor')
            if instructor_group in user.groups.all():
                auth_login(request, user)
                # messages.success(request, f'Login successful.')
                return redirect('instbase')  
            else:
                messages.error(request, f'Sorry, you are not authorized to login as an Instructor.')
                return redirect('login')
        else:
            messages.error(request, f'Invalid username or password.')
    
        messages.error(request, f'Fill in the form correctly.')
   
    return render(request, 'users/instructorlogin.html') 

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            # Check if the user belongs to the 'admin' group
            admin_group = Group.objects.get(name='admin')
            if admin_group in user.groups.all():
                auth_login(request, user)
                return redirect('index')  
            else:
                messages.error(request, f'Sorry, you are not authorized to login as an Admin.')
                return redirect('login')
        else:
            messages.error(request, f'Invalid username or password.')
    
        messages.error(request, f'Fill in the form correctly.')
   
    return render(request, 'users/adminlogin.html') 

