import os
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from instructor.models import Event
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.models import Group
# **html2pdf imports
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from users.models import CustomUser
from vantage import settings
from datetime import date
from trainee.models import Booking
from instructor.forms import EditProfileForm

@login_required(login_url='instructorlogin')
def instbase(request):
    return render(request, 'instructor/instbase.html')

@login_required(login_url='instructorlogin')
def landing(request):
    return render(request, 'instructor/landing.html')

@login_required(login_url='instructorlogin')
def myprofile(request):
    return render(request, 'instructor/myprofile.html')

def logoutUser(request):
     logout(request)
     return redirect('login')


@login_required(login_url='instructorlogin')
def calendar(request):
    all_events = Event.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'instructor/calendar.html',context)

def all_events(request):                                                                                                 
    all_events = Event.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        start_date = event.start.strftime("%Y-%m-%dT%H:%M:%S") if event.start else None
        end_date = event.end.strftime("%Y-%m-%dT%H:%M:%S") if event.end else None
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': start_date,                                                                                         
            'end': end_date,                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False)

def booked_events(request):
    # Get the trainee's booked events
    trainee_bookings = Booking.objects.filter(trainee=request.user)
    
    # Convert the booked events into the format expected by FullCalendar
    booked_events_data = []
    for booking in trainee_bookings:
        start_date = booking.event.start.strftime("%Y-%m-%dT%H:%M:%S") if booking.event.start else None
        end_date = booking.event.end.strftime("%Y-%m-%dT%H:%M:%S") if booking.event.end else None
        booked_events_data.append({
            'title': booking.event.name,  # Include the event name (title)
            'id': booking.event.id,
            'start': start_date,
            'end': end_date,
        })
    
    return JsonResponse(booked_events_data, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    
    # Check if user is authenticated
    if request.user.is_authenticated:
        instructor_id = request.user.id  # Get the instructor's ID from the logged-in user
        event = Event(name=str(title), start=start, end=end, instructor_id=instructor_id)
        event.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated'}, status=401)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

@login_required(login_url='instructorlogin') 
def show_trainees(request):
    # Get the "trainee" group
    trainee_group = Group.objects.get(name='trainee')
    
    # Get all users who belong to the "trainee" group
    trainees = trainee_group.user_set.all().order_by('id')
    
    context = {
        'users': trainees
    }

    return render(request, 'instructor/traineelist.html', context)

@login_required(login_url='instructorlogin')
def trainee_pdf_create(request):
    trainee_group = Group.objects.get(name='trainee')
    trainees = trainee_group.user_set.all().order_by('id')

    template_path = 'instructor/traineelistpdf.html'

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

from .models import Event, CustomUser  # Import the necessary models

@login_required(login_url='instructorlogin') 
def show_lessons(request):
    # Fetch events from the tblevents table
    events = Event.objects.all()

    # Fetch instructor names for each event
    for event in events:
        instructor = CustomUser.objects.get(pk=event.instructor_id)
        event.instructor_name = instructor.username

    context = {
        'events': events
    }

    return render(request, 'instructor/lessons.html', context)


@login_required(login_url='instructorlogin')
def lessons_pdf_create(request):
    events = Event.objects.all()

    template_path = 'instructor/lessonspdf.html'

     # Get the current date
    today_date = date.today().strftime("%B %d, %Y")

    context = {
        'events': events,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'date': today_date  # Include the current date in the context  
    
     }

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="LessonList.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='instructorlogin')
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
           
            messages.success(request, f'Your details have been updated successfully')
            return redirect('/instructor/myprofile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render (request, 'instructor/editprofile.html', args)

@login_required(login_url='instructorlogin')
def changeprofile(request): 
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your password has been changed successfully')
            return redirect('/instructor/myprofile')            
        else:
            messages.success(request, f'Your current password is wrong. Try again')
            return redirect('/instructor/myprofile')
    
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render (request, 'instructor/changeprofile.html', args)
    
def printprofile(request):
    # Get the currently logged-in user
    user = request.user

    # Fetch additional details from the CustomUser model
    user = CustomUser.objects.get(pk=user.pk)  # Assuming CustomUser has a primary key 'pk'   

    template_path = 'instructor/pdfprofile.html'
    # Render the template with the bookings data
    # Get the current date
    today_date = date.today().strftime("%B %d, %Y")

    context = {
        'user': user,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png'),
        'date': today_date  # Include the current date in the context 
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="InstructorProfile.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response    