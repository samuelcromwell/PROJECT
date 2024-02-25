from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'adminview/index.html')
def logoutUser(request):
     logout(request)
     return redirect('login') 
def traineelist(request):
     return render(request, 'adminview/traineelist.html') 