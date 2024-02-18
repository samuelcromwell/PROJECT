from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from instructor.models import Events

@login_required
def instbase(request):
    return render(request, 'instructor/instbase.html')
def profile(request):
    return render(request, '')
def logoutUser(request):
     logout(request)
     return redirect('login')
def calendar(request):
    return render(request, 'instructor/calendar.html')
def calbase(request):
    return render(request, 'instructor/calbase.html')

   
