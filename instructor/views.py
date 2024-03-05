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

# def add_event(request):
#     start = request.GET.get("start", None)
#     end = request.GET.get("end", None)
#     title = request.GET.get("title", None)

#     # Convert start and end strings to datetime objects
#     start_datetime = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
#     end_datetime = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')

#     # Get the current datetime
#     current_datetime = datetime.now()

#     # Check if start or end date is before the current date
#     if start_datetime < current_datetime or end_datetime < current_datetime:
#         # If so, return an error response
#         return JsonResponse({'error': 'Cannot add event to a date before the current day'}, status=400)

#     # If the start and end dates are valid, proceed to create the event
#     event = Events(name=str(title), start=start, end=end)
#     event.save()
#     data = {}
#     return JsonResponse(data)

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