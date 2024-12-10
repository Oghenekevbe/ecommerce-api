from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from store.models import Cart
from store.serializers import CartSerializer
from .serializers import PaymentSerializer
import requests
import math
import random
import hashlib
import json

# Create your views here.


class OrderPayment(APIView):
    model = Cart
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        order = self.get_object(user)
        print("order : ", order)
        data = request.data
        print("data = ", data)
        print("mode of payment: ", data.get("mode_of_payment"))
        if data.get("mode_of_payment") == "flutterwave":
            pay_with_flutterwave(order)
            serializer = PaymentSerializer(data=data)
            response = {
                'data' : serializer.data,
                'message' : f"Redirecting you to {data.get("mode_of_payment")}'s payment portal"
            }
            return Response(data = response, status=status.HTTP_200_OK)
        
        elif data.get("mode_of_payment") == "paystack":
            pay_with_paystack(order)
            serializer = PaymentSerializer(data=data)
            response = {
                'data' : serializer.data,
                'message' : f"Redirecting you to {data.get("mode_of_payment")}'s payment portal"
            }
            return Response(data = response, status=status.HTTP_200_OK)
        
        elif data.get("mode_of_payment") == "remita":
            pay_with_remita(order)
            
            serializer = PaymentSerializer(data=data)
            response = {
                'data' : serializer.data,
                'message' : f"Redirecting you to {data.get("mode_of_payment")}'s payment portal"
            }
            return Response(data = response, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {"error": "Invalid payment mode"}, status=status.HTTP_400_BAD_REQUEST
            )


    def get_object(self, user):
        return get_object_or_404(self.model, is_active=True, user=user)



def pay_with_paystack(order):
    email = order.user.email
    amount = float(order.cart_total * 100)
    first_name = ""
    last_name = ""

    # Initialize payment with Paystack
    paystack_url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_KEY}",
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
        payment_url = payment_data.get("data", {}).get("authorization_url")
        if payment_url:
            print(payment_data)  # Print payment data for debugging
            print(payment_url)  # Print payment URL for debugging
            return redirect(payment_url)
        else:
            return JsonResponse(
                {"error": "Payment URL not found in response"}, status=400
            )
    else:
        return JsonResponse({"error": "Failed to initialize payment"}, status=400)





def pay_with_remita(order):
    email = order.user.email
    amount = float(order.cart_total * 100)

    orderId = (
        str(order.order_number) + "/" + str(math.ceil(random.randint(1, 1000000)))
    )
    remita_url = "https://remitademo.net/remita/exapp/api/v1/send/api/echannelsvc/merchant/api/paymentinit"


    concatenated_values = (
        f"{settings.REMITA_CREDENTIALS['merchantId']}"
        f"{settings.REMITA_CREDENTIALS['serviceTypeId']}"
        f"{orderId}"
        f"{amount}"
        f"{settings.REMITA_CREDENTIALS['apiKey']}"
    )        
    # Compute the SHA-512 hash
    apiHash = hashlib.sha512(concatenated_values.encode()).hexdigest()

    print('api hash: ', apiHash)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"remitaConsumerKey={settings.REMITA_CREDENTIALS['merchantId']},remitaConsumerToken={apiHash}"
    }


    payload = { 
        "serviceTypeId": "4430731",
        "amount": amount,
        "orderId": orderId,
        "payerName": str(order.order_number),
        "payerEmail": email,
        "payerPhone": "",
        "description": "Payment for " + str(order.order_number)
    }

    print('payload = ', payload)

    response = requests.post(remita_url, json=payload, headers=headers)
    try:
        response_json = response.json()
        if response.status_code == 200:
            print("Payment successful. Response:", response_json)
        else:
            print("Failed to make payment. Status code:", response.status_code)
            print("Response:", response_json)
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        print("Response content:", response.content)




def pay_with_paypal(order):
    email = order.user.email
    amount = float(order.cart_total * 100)
    address = order.address.get(is_billing_address = True)

    orderId = (
        str(order.order_number) + "/" + str(math.ceil(random.randint(1, 1000000)))
    )


    payment_url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': str(order.order_number),
        'Authorization': f'Basic {settings.PAYPAL_Client_ID}',
    }

    data = { 
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b",
                "amount": {
                    "currency_code": "USD",
                    "value": amount
                }
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "brand_name": "E-commerce Online Shopping",
                    "locale": "en-US",
                    "landing_page": "",
                    "shipping_preference": address,
                    "user_action": "PAY_NOW",
                    "return_url": f"https://api-m.paypal.com/v2/checkout/orders/{orderId}/capture",
                    "cancel_url": ""
                }
            }
        }
    }


    response = requests.post(payment_url, headers=headers, json=data)



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
