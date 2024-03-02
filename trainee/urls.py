from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.base, name="base"),
    path('logout/',views.logoutUser, name="logout"),   
    path('profile/',views.profile, name="profile"),   
    path('profile/edit',views.edit, name="edit"),   
    path('profile/changepassword',views.change, name="change"),   
    
]