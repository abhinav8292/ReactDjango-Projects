from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import json

stripe.api_key = "sk_test_51IeDvNSACUKPl95IzajsHJPBYPdheA3MOXUrayAi5XqsDYVgw8QW7G3aoQrw7ElAnEoMwDMhr8ww5yiV8qeZYlqV005BoM4wIe"

# Create your views here.


@csrf_exempt
def payment(request):
    try:
        if request.method == "POST":
            totalAmount = json.loads(request.body)
            intent = stripe.PaymentIntent.create(
                amount=round(totalAmount),
                currency='inr',
                payment_method_types=["card"]
            )
            print("intent", intent)

        return JsonResponse({
            'clientSecret': intent['client_secret']
        })

    except Exception as e:
        return JsonResponse({"error": str(e)})
