import os
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from instructor.models import Events
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

@login_required(login_url='instructorlogin')
def instbase(request):
    return render(request, 'instructor/instbase.html')

@login_required(login_url='instructorlogin')
def landing(request):
    return render(request, 'instructor/landing.html')

def logoutUser(request):
     logout(request)
     return redirect('login')


@login_required(login_url='instructorlogin')
def calendar(request):
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'instructor/calendar.html',context)

def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
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


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
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

    context = {
        'users': trainees,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
    
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

@login_required(login_url='instructorlogin') 
def show_lessons(request):
# Fetch events from the tblevents table
    events = Events.objects.all()

    context = {
        'events': events
    }

    return render(request, 'instructor/lessons.html', context)

@login_required(login_url='instructorlogin')
def lessons_pdf_create(request):
    events = Events.objects.all()

    template_path = 'instructor/lessonspdf.html'

    context = {
        'events': events,
        'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
    
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