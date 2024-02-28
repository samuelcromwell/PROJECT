from django.db import models
from users.models import CustomUser  # Import the CustomUser model if it's in a different app

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    instructorname = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def first_name(self):
        return self.instructor.first_name if self.instructor else None

    class Meta:  
        db_table = "tblevents"
