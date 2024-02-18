from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.instbase, name="instbase"),
    path('logout/',views.logoutUser, name="logout"),   
    path('profile/',views.profile, name="profile"),   
    path('calendar/',views.calendar, name="calendar"),
    path('calendarpreview/',views.calbase, name="calbase"),

]