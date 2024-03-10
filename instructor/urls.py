from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.instbase, name="instbase"),
    path('logout/',views.logoutUser, name="logout"),      
    path('calendar/',views.calendar, name="calendar"),    
    path('home/',views.landing, name="landing"),
    path('showtrainees', views.show_trainees, name='showtrainees'),
    path('traineepdf', views.trainee_pdf_create, name='traineepdf'),
    

]