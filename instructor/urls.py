from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.instbase, name="instbase"),
    path('logout/',views.logoutUser, name="logout"),      
    path('calendar/',views.calendar, name="calendar"),
]    