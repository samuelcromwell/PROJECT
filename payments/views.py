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
