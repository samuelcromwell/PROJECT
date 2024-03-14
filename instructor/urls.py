from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.instbase, name="instbase"),
    path('logout/',views.logoutUser, name="logout"),      
    path('calendar/',views.calendar, name="calendar"),    
    path('home/',views.landing, name="landing"),
    path('showtrainees/', views.show_trainees, name='showtrainees'),
    path('showlessons/', views.show_lessons, name='showlessons'),
    path('traineepdf/', views.trainee_pdf_create, name='traineepdf'),
    path('lessonpdf/', views.lessons_pdf_create, name='lessonpdf'),
    path('myprofile/',views.myprofile, name="myprofile"),
    path('myprofile/edit',views.editprofile, name="editprofile"), 
    path('myprofile/changepassword',views.changeprofile, name="changeprofile"),
    path('printprofile/', views.printprofile, name='printprofile'),
]