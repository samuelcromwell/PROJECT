from django.urls import path, include
from . import views

urlpatterns = [   
    path('', views.index, name="index"),
    path('logout/',views.logoutUser, name="logout"), 
    path('trainees/',views.trainees, name="trainees"), 
    path('traineespdf/',views.traineespdf, name="traineespdf"), 
    path('traineelist/',views.traineelist, name="traineelist"),
    path('profileee/',views.profileee, name="profileee"),
    path('payments/',views.payments, name="paymentsss"),
    

]