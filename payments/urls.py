from django.urls import path, include
from . import views

urlpatterns = [
    # Other URL patterns
    path('payment/', views.payment_page, name='payment_page'), 
]