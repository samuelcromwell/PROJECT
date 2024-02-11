from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required
def base(request):
    return render(request, 'trainee/base.html')
def profile(request):
    return render(request, 'trainee/profile.html')
def logoutUser(request):
     logout(request)
     return redirect('login')

   
