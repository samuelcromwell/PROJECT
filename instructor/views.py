from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from instructor.models import Events
from django.http import JsonResponse
from datetime import datetime
from .forms import ProgressUpdateForm

def instbase(request):
    return render(request, 'instructor/instbase.html')

def landing(request):
    return render(request, 'instructor/landing.html')

def logoutUser(request):
     logout(request)
     return redirect('login')

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
 



def progress(request):
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Progress Updated')
            return redirect('progress')       
    else:
        form = ProgressUpdateForm()
    return render(request, 'instructor/progress.html', {'form': form})