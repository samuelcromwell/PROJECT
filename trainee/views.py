import os
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from trainee.forms import EditProfileForm
from adminview.models import TraineePayment
from instructor.models import Events
from users.models import CustomUser
from vantage import settings

# **html2pdf imports
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView


#sample view
def render_pdf_view(request):
    template_path = 'trainee/pdf1.html'
    context = {'myvar': 'this is your template context'}
    
    # Render the HTML template
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a Django response object with content type set to PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'  # Change to 'inline'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Check for errors
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response



@login_required(login_url='traineelogin')
def base(request):
    return render(request, 'trainee/base.html')

@login_required(login_url='traineelogin')
def home(request):
    return render(request, 'trainee/landing.html')



@login_required(login_url='traineelogin')
def book(request):
    return render(request, 'trainee/book.html')

@login_required(login_url='traineelogin')
def profile(request):
    return render(request, 'trainee/profile.html')

# @login_required(login_url='traineelogin')
def logoutUser(request):
     logout(request)
     return redirect('login')

@login_required(login_url='traineelogin')
def edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
           
            messages.success(request, f'Your details have been updated successfully')
            return redirect('/trainee/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render (request, 'trainee/edit.html', args)

@login_required(login_url='traineelogin')
def change(request): 
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your password has been changed successfully')
            return redirect('/trainee/profile')            
        else:
            messages.success(request, f'Your current password is wrong. Try again')
            return redirect('/trainee/profile')
    
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render (request, 'trainee/change.html', args)
    

@login_required(login_url='traineelogin')
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
    return render(request, 'trainee/payments.html', context)

@login_required(login_url='traineelogin')
def book(request):
    events = Events.objects.all()
    return render(request, 'trainee/book.html', {'events': events})        



@login_required(login_url='traineelogin')
def fullcalendar(request):
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'trainee/fullcalendar.html',context)

@login_required(login_url='traineelogin')
def print_payments(request):
    # Get details of the currently logged-in user
    user = request.user
    payments = TraineePayment.objects.filter(trainee=user)
    total_paid = sum(payment.amount_paid for payment in payments)
    initial_balance = 20000  # Assuming initial balance is 20000    

    # Fetch additional details from the CustomUser model
    user = CustomUser.objects.get(pk=user.pk)  # Assuming CustomUser has a primary key 'pk'

    template_path = 'trainee/paymentspdf.html'

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
        'user': user,
        'payments': payments,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'trainee_payments': updated_payments,
        'total_paid': total_paid,
        'current_balance': balance        
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Payments.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    