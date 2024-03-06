from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db.models import Sum

class TraineePayment(models.Model):
    trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'trainee'}, related_name='trainee_payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Allow null values for dynamic calculation
    payment_date = models.DateField(default=timezone.now)  # Set default value to today's date

    def __str__(self):
        return f"Payment for {self.trainee.username}"


