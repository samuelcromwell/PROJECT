from django import forms
from django.core.exceptions import ValidationError
from .models import TraineePayment
from django.db.models import Sum

class PaymentForm(forms.ModelForm):
    initial_fee = forms.DecimalField(initial=20000, disabled=True)
    balance = forms.DecimalField(disabled=True, required=False)
    
    class Meta:
        model = TraineePayment
        fields = ['trainee', 'initial_fee', 'amount_paid', 'balance']

    def clean(self):
        cleaned_data = super().clean()
        initial_fee = cleaned_data.get('initial_fee')
        amount_paid = cleaned_data.get('amount_paid')
        trainee = cleaned_data.get('trainee')

        if trainee:
            previous_payments = TraineePayment.objects.filter(trainee=trainee)
            total_paid = previous_payments.aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0
            previous_balance = initial_fee - total_paid
            if previous_balance is not None:
                cleaned_data['balance'] = previous_balance - amount_paid
            else:
                cleaned_data['balance'] = initial_fee - amount_paid

            if cleaned_data['balance'] < 0:
                raise ValidationError("The amount being paid is more than the balance due.")
                
        return cleaned_data
