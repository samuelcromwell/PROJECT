"""
URL configuration for vantage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from instructor.urls import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('trainee/', include('trainee.urls')),
    path('instructor/', include('instructor.urls')),
    path('adminview/', include('adminview.urls')),
    path('payments/', include('payments.urls')),
    path('all_events/', views.all_events, name="all_events"),
    path('booked_events/', views.booked_events, name="booked_events"),
    path('add_event/', views.add_event, name="add_event"), 
    path('update/', views.update, name="update"),
    path('remove/', views.remove, name="remove"),    
]


#youtube video
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()