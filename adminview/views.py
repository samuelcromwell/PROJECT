import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from adminview.models import TraineePayment
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

def profileee(request):
    return render(request, 'adminview/profileee.html')  

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

@login_required(login_url='adminviewlogin') 
def traineelist(request):
    # Get the "trainee" group
    trainee_group = Group.objects.get(name='trainee')
    
    # Get all users who belong to the "trainee" group
    trainees = trainee_group.user_set.all().order_by('id')
    
    context = {
        'users': trainees
    }

    return render(request, 'adminview/traineelist.html', context)

def payments(request):
    trainee = request.user
    payments = TraineePayment.objects.filter(trainee=trainee)
    total_paid = sum(payment.amount_paid for payment in payments)
    initial_balance = 20000  # Assuming initial balance is 20000

    # Calculate balance after each payment
    balance = initial_balance
    updated_payments = []
    for payment in payments:
        balance -= payment.amount_paid
        updated_payments.append({
            'payment_date': payment.payment_date,
            'amount_paid': payment.amount_paid,
            'balance': balance
        })

    context = {
        'trainee_payments': updated_payments,
        'total_paid': total_paid,
        'current_balance': balance
    }
    return render(request, 'adminview/payments.html', context) 