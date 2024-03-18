from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import MpesaPayment

from django_daraja.mpesa.core import MpesaClient
import json
# from .mpesa.core import verify_payment
# from .mpesa.status import MpesaStatus
from datetime import timedelta, datetime


def payment_page(request):
    return render(request, 'payments/payment_page.html')

# def process_payment(request):
#     BASE_URL = 'https://c7da-41-212-76-10.ngrok-free.app'

#     if request.method == 'POST':
#         user_id = request.user.id

#         phone = request.POST.get('phone')
#         # cl = MpesaClient()
#         # # amount = int(subscription_plan.price)
#         # account_reference = 'reference'
#         # transaction_desc = 'Description'
#         # # callback_url = BASE_URL + f'/subscription_confirmation/{user_id}/{plan_id}/'
        
#         # # response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
#         # print(f'The response code is:{response.response_code}')
#         # if response.response_code == "0":
#         #     mpesa_payment = MpesaPayment.objects.create(user=request.user, subscription=subscription_plan, reference_id=response.checkout_request_id)
#         #     return redirect('confirm_payment', mpesa_payment.id)
#         # else:
#             # messages.error(request, "We couldn't process your payment")
#         return redirect('payments/payment_page.html')
        