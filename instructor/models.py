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

class Progress(models.Model):
    # trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'trainee'}, related_name='trainee_payments')
    trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # lesson_name = models.ForeignKey(Events, on_delete=models.CASCADE)  # ForeignKey to Events model
    progress_percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"Progress for {self.trainee.username} - Lesson: {self.lesson_name.name}"

