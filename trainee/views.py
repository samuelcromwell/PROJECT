from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from instructor.models import Progress
from trainee.forms import EditProfileForm
from adminview.models import TraineePayment
from instructor.models import Events

@login_required(login_url='traineelogin')
def base(request):
    return render(request, 'trainee/base.html')

@login_required(login_url='traineelogin')
def home(request):
    return render(request, 'trainee/landing.html')

@login_required(login_url='traineelogin')
def viewprogress(request):
    return render(request, 'trainee/viewprogress.html')

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
def viewprogress(request):
    trainee_progress = Progress.objects.filter(trainee=request.user)
    return render(request, 'trainee/viewprogress.html', {'trainee_progress': trainee_progress})

@login_required(login_url='traineelogin')
def fullcalendar(request):
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'trainee/fullcalendar.html',context)


