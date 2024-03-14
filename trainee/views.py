import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from trainee.forms import EditProfileForm
from adminview.models import TraineePayment
from instructor.models import Event
from users.models import CustomUser
from vantage import settings
from django.utils import timezone
from datetime import date
# **html2pdf imports
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from . models import Booking

@login_required(login_url='traineelogin')
def base(request):
    return render(request, 'trainee/landing.html')

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
def fullcalendar(request):
    all_events = Event.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'trainee/fullcalendar.html',context)

@login_required(login_url='traineelogin')
def calendarschedule(request):
    # Get trainee's booked events
    trainee_bookings = Booking.objects.filter(trainee=request.user)
    
    # Format events for FullCalendar
    formatted_events = []
    for booking in trainee_bookings:
        formatted_event = {
            'id': booking.event.id,
            'name': booking.event_name,
            'start': booking.event.start.isoformat(),
            'end': booking.event.end.isoformat(),
            # Add any other necessary fields
        }
        formatted_events.append(formatted_event)
    
    context = {
        "events": formatted_events,
    }
    return render(request, 'trainee/calendarschedule.html', context)
    
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

     # Get the current date
    today_date = date.today().strftime("%B %d, %Y")

    context = {
        'user': user,
        'payments': payments,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'trainee_payments': updated_payments,
        'total_paid': total_paid,
        'current_balance': balance, 
        'date': today_date  # Include the current date in the context   
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

@login_required(login_url='traineelogin')
def book(request):
    events = Event.objects.all()
    return render(request, 'trainee/book.html', {'events': events})   


@login_required(login_url='traineelogin')
def book_event(request, event_id):
    # Retrieve the event object based on the event ID
    event = get_object_or_404(Event, pk=event_id)
    
    # Check if the trainee has already booked the event
    if Booking.objects.filter(trainee=request.user, event=event).exists():
        # Trainee has already booked the event, display an error message
        messages.error(request, '⚠️ You have already booked this event ⚠️')
        return redirect('event_list')  # Redirect to the event list page or wherever appropriate
    
    # Check if the event end datetime is after the current datetime
    if event.end >= timezone.now():
        # Create a new booking entry associating the current trainee with the selected event
        booking = Booking.objects.create(trainee=request.user, event=event)
        # Optionally, you can perform additional actions here, such as sending a confirmation email to the trainee
        
        # Display a success message
        messages.success(request, '✅ Lesson booked successfully! ✅')
        return redirect('event_list')  # Redirect the user to a page showing the list of events
    else:
        # If the event has already ended, display an error message
        messages.error(request, '⚠️ You cannot book past events ⚠️')
        return redirect('event_list')  # Redirect to the event list page or wherever appropriate

@login_required(login_url='traineelogin')
def showlessons(request):
    # Get bookings for the logged-in user
    user = request.user
    bookings = Booking.objects.filter(trainee=user)

    # Fetch instructor names for each booking
    for booking in bookings:
        event = Event.objects.get(pk=booking.event_id)
        instructor = CustomUser.objects.get(pk=event.instructor_id)
        booking.instructor_name = instructor.username

    context = {
        'bookings': bookings,
    }

    return render(request, 'trainee/schedule.html', context)



def print_schedule(request):
    # Get the currently logged-in user
    user = request.user

    # Fetch additional details from the CustomUser model
    user = CustomUser.objects.get(pk=user.pk)  # Assuming CustomUser has a primary key 'pk'


    # Retrieve bookings for the logged-in user
    bookings = Booking.objects.filter(trainee=user)

    template_path = 'trainee/schedulepdf.html'
    # Render the template with the bookings data
    # Get the current date
    today_date = date.today().strftime("%B %d, %Y")

    context = {
        'user': user,
        'bookings': bookings,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'date': today_date  # Include the current date in the context 
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Schedule.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def print_profile(request):
    # Get the currently logged-in user
    user = request.user

    # Fetch additional details from the CustomUser model
    user = CustomUser.objects.get(pk=user.pk)  # Assuming CustomUser has a primary key 'pk'   

    template_path = 'trainee/profilepdf.html'
    # Render the template with the bookings data
    # Get the current date
    today_date = date.today().strftime("%B %d, %Y")

    context = {
        'user': user,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'date': today_date  # Include the current date in the context 
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="MyProfile.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def delete_booking(request, booking_id):
    # Retrieve the booking object based on the booking ID
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Check if the booking belongs to the current user or if the user has permission to delete bookings
    # You may need to customize this logic based on your requirements
    
    # Delete the booking
    booking.delete()
    
    # Optionally, you can add a success message to indicate that the booking has been deleted
    # messages.success(request, 'Booking deleted successfully.')
    
    # Redirect the user to a page showing the list of bookings or any other appropriate page
    return redirect('event_list')
