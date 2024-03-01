import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser
from django.contrib.auth.models import Group

@login_required
def index(request):
    return render(request, 'adminview/index.html')
# @login_required
def logoutUser(request):
     logout(request)
     return redirect('login') 
@login_required
def traineelist(request):
    trainee_group = Group.objects.get(name='trainee')
    trainee_users = CustomUser.objects.filter(groups=trainee_group)
    context = {
        'traineelist': trainee_users,
    }

    return render(request, 'adminview/traineelist.html', context)

