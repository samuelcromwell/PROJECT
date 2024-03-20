from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model
from instructor.models import Event
from django.utils import timezone
from django.db import models
from users.models import CustomUser
    

#add your models here

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
    ]

    trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)  # Date and time when the booking is made
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def event_name(self):
        return self.event.name  # Assuming the Event model has a 'name' field

    def duration(self):
        return self.event.end - self.event.start  # Assuming 'start' and 'end' are DateTimeField in Event model
    
    def event_start(self):
        return self.event.start  # Assuming the Event model
    
    def event_end(self):
        return self.event.end  # Assuming the Event model
    
    def __str__(self):
        return f"Booking for {self.event} by {self.trainee}"


class MpesaPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')    
    date = models.DateTimeField(default=timezone.now)
