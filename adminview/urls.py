from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.logoutUser, name="logout"), 
    path('traineelist/', views.traineelist, name="traineelist"),     
    path('register_instructor/', views.reginstructor, name="reginstructor"),     

]