import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site



def pay_with_paystack(order):
    email = order.user.email
    amount = float(order.cart_total * 100)
    address = order.address
    order_number = order.order_number

    # Initialize payment with Paystack
    paystack_url = "https://api.paystack.co/transaction/initialize"   
    domain = get_current_site(request).domain

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": amount,
        "order_number" : order_number,
        "currency" : "NGN",
        'callback_url' : f"http://{domain}/payments/call-back/",
        'metadata': {
            'address': address
           
        }
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
    




def verify_payment(reference):
    """
    Verify payment with Paystack using the provided reference.
    """
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_KEY}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(verify_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        verify_data = response.json()
        
        if verify_data.get('status') and verify_data.get('data').get('status') == 'success':
            return verify_data['data']
        else:
            return None
    except requests.RequestException as e:
        print(f"Error verifying payment: {e}")
        return None

