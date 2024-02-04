from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name="home"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('login/', views.login, name="login"),
    path('courses/', views.courses, name="courses"),
    path('signup/', views.signup, name="signup"),
    path('traineelogin/', views.traineelogin, name="traineelogin"),
    path('admin/', views.admin, name="admin"),
]

    #path('admin/', views.admin, name="admin"),
    #path('accounts/', include('django.contrib.auth.urls')),  # Include Django's authentication URLs
