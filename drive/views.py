from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def base(request):
    return render(request, 'drive/base1.html')
def maintest(request):
    return render(request, 'drive/maintest.html')

   
