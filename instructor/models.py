from django.db import models
from users.models import CustomUser

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')
        
    class Meta:  
        db_table = "tblevents"
