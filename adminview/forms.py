from django import forms
from .models import TraineePayment

class PaymentForm(forms.ModelForm):
    amount_due = forms.DecimalField(initial=20000, disabled=True)
    balance = forms.DecimalField(disabled=True, required=False)

    class Meta:
        model = TraineePayment
        fields = ['trainee', 'amount_due', 'amount_paid', 'balance']

    def clean(self):
        cleaned_data = super().clean()
        amount_due = cleaned_data.get('amount_due')
        amount_paid = cleaned_data.get('amount_paid')
        if amount_due is not None and amount_paid is not None:
            cleaned_data['balance'] = amount_due - amount_paid
        return cleaned_data
