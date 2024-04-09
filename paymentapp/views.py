from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from store.models import Cart
from store.serializers import CartSerializer
import requests
import math
import random

# Create your views here.


class OrderPayment(APIView):

    permission_classes = [permissions.IsAuthenticated]
    model = Cart

    def post(self, request, *args, **kwargs):
        user = request.user
        order = self.get_object(user)
        print("order : ", order)
        data = request.data
        print("data = ", data)
        print("mode of payment: ", data.get("mode_of_payment"))
        if data.get("mode_of_payment") == "flutterwave":
            make_payment(order)
            return Response({"message": "You will be redirected to flutterwave site"})

    def get_object(self, user):
        return get_object_or_404(self.model, is_active=True, user=user)


def make_payment(order):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
    }

    reference = (
        str(order.order_number) + "/" + str(math.ceil(random.randint(1, 1000000)))
    )

    payload = {
        "tx_ref": reference,
        "amount": float(order.cart_total),
        "currency": order.cart_items.first().product.currency,
        "redirect_url": "http://127.0.0.1:8000/api/payment_completed/",
        "payment_options": "card",
        "meta": {"source": "docs-inline-test", "consumer_mac": "92a3-912ba-1192a"},
        "customer": {
            "email": order.user.email,
            "phone_number": "08100000000",
            "name": order.user.username,
        },
        "customizations": {
            "title": "E-commerce Online Shopping",
            "description": "Payment for " + str(order.order_number),
            "logo": "https://checkout.flutterwave.com/assets/img/rave-logo.png",
        },
    }
    print("payload:  ", payload)
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        payment_response = response.json()
        print("Payment successful!")
        print("Payment details:", payment_response)
    else:
        print("Failed to make payment. Status code:", response.status_code)


def pay_with_paystack(request):
    email = request.POST.get("email")
    amount = request.POST.get("amount")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")

    # Initialize payment with Paystack
    paystack_url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": "Bearer YOUR_SECRET_KEY",  # Replace with your secret key
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": amount,
        "metadata": {
            "first_name": first_name,
            "last_name": last_name,
        },
    }
    response = requests.post(paystack_url, headers=headers, json=data)

    if response.status_code == 200:
        payment_data = response.json()
        # You can save payment data or send it to the frontend for further processing
        return JsonResponse(payment_data)
    else:
        return JsonResponse({"error": "Failed to initialize payment"}, status=400)


class orderCompletedView(APIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            order = Cart.objects.get(user=user, is_active=True)
            for item in order.cart_items.all():
                item.status = "confirmed"
                item.save()
            order.status = "confirmed"
            order.is_active = False  # Set the cart as inactive
            order.save()
        except Cart.DoesNotExist:
            pass

        # Create a new empty cart for the user
        new_order = Cart.objects.create(user=user)
        new_order.save()
        response = {"message": "Payment Successful"}
        return Response(data=response, status=status.HTTP_200_OK)
