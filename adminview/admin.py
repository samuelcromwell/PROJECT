from django.contrib import admin
from .models import TraineePayment
from .forms import PaymentForm

class TraineePaymentAdmin(admin.ModelAdmin):
    form = PaymentForm

admin.site.register(TraineePayment, TraineePaymentAdmin)