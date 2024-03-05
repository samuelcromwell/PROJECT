from django.db import models
from users.models import CustomUser  # Import the CustomUser model if it's in a different app
from django.contrib.auth.models import User
from django.conf import settings

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def first_name(self):
        return self.instructor.first_name if self.instructor else None

    class Meta:  
        db_table = "tblevents"



class Course(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed

class Progress(models.Model):
    trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
