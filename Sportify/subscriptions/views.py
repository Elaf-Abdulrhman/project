# subscriptions/views.py

import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .models import Payment
from django.contrib.auth.decorators import login_required
from account.models import Club
from django.http import JsonResponse

@login_required
def payment_success(request):
    payment_id = request.GET.get('id')  # Get the payment ID from the query parameters

    if not payment_id:
        return render(request, 'subscriptions/payment_failed.html', {'error': 'Missing payment ID'})

    # Verify the payment with Moyasar API
    moyasar_secret_key = 'sk_test_sF2ML8JKf8QhAL7mrtVBrgXs5p4tjKvVrhFXLJG1'
    response = requests.get(
        f'https://api.moyasar.com/v1/payments/{payment_id}',
        auth=(moyasar_secret_key, '')
    )

    if response.status_code != 200:
        return render(request, 'subscriptions/payment_failed.html', {'error': 'Payment not completed'})

    payment_data = response.json()

    # Save the payment data locally
    is_premium = payment_data['status'] == 'paid'  # Set is_premium to True if payment is successful
    Payment.objects.create(
        user=request.user,
        payment_id=payment_data['id'],
        amount=payment_data['amount'] / 100,  # Convert from halalas to SAR
        status=payment_data['status'],
        is_premium=is_premium,
    )

    # Redirect to success page if payment is successful
    if payment_data['status'] == 'paid':
        # Retrieve the Club instance associated with the user
        try:
            club = Club.objects.get(user=request.user)  # Assuming a one-to-one relationship between Club and User
            club.is_premium = True
            club.save()
        except Club.DoesNotExist:
            return render(request, 'subscriptions/payment_failed.html', {'error': 'Club not found'})

        return render(request, 'subscriptions/payment_success.html', {'payment': payment_data})
    else:
        return render(request, 'subscriptions/payment_failed.html', {'error': 'Payment failed'})


def payment(request):
    return render(request, 'subscriptions/payment.html', {
        'moyasar_publishable_key': settings.MOYASAR_PUBLISHABLE_KEY,
    })


def plus_plan(request):
    return render(request, 'subscriptions/plus_plan.html')
