from django.contrib import admin
from .models import TraineePayment
from .forms import PaymentForm

class TraineePaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('first_name', 'amount_paid', 'balance')

    def first_name(self, obj):
        return obj.trainee.first_name
    
    def balance(self, obj):
        return obj.balance  # Assuming balance is already calculated and stored in the TraineePayment model

admin.site.register(TraineePayment, TraineePaymentAdmin)
