from django.utils import timezone
from django.db import models
from users.models import CustomUser
    
class MpesaPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')    
    date = models.DateTimeField(default=timezone.now)
