from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name="index"),
    path('logout/',views.logoutUser, name="logout"), 
    path('traineelist/',views.traineelist, name="traineelist"), 
    
]