import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser
from django.contrib.auth.models import Group
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from vantage import settings
from datetime import date

@login_required
def trainees(request):
     # Get the "trainee" group
    trainee_group = Group.objects.get(name='trainee')
    
    # Get all users who belong to the "trainee" group
    trainees = trainee_group.user_set.all().order_by('id')
    
    context = {
        'users': trainees
    }

    return render(request, 'adminview/trainees.html', context)

def index(request):
    return render(request, 'adminview/index.html')  

def logoutUser(request):
    logout(request)
    return redirect('login')

def traineespdf(request):
    trainee_group = Group.objects.get(name='trainee')
    trainees = trainee_group.user_set.all().order_by('id')

    template_path = 'adminview/traineespdf.html'

     # Get the current date
    today_date = date.today().strftime("%B %d, %Y")

    context = {
        'users': trainees,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'date': today_date  # Include the current date in the context  
    
     }

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="TraineeList.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
