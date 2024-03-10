from django.db import models
from users.models import CustomUser  # Import the CustomUser model if it's in a different app
from django.contrib.auth.models import User
from django.conf import settings

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
        
    class Meta:  
        db_table = "tblevents"



