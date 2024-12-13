
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from store.models import Cart
from store.serializers import CartSerializer
from .serializers import PaymentSerializer
from services.payment_services import pay_with_paystack, verify_payment
from services.service_responses import *

class OrderPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        order = Cart.objects.get_or_create(user=user, is_active = True)
        print("order : ", order)
        data = request.data
        print("data = ", data)
        if data:
        
            pay_with_paystack(order)
            serializer = PaymentSerializer(data=data)
            response = {
                'data' : serializer.data,
                'message' : f"Redirecting you to paystack payment portal"
            }
            return Response(data = response, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {"error": "invalid"}, status=status.HTTP_400_BAD_REQUEST
                
            )





@api_view(['GET'])
def payment_callback(request):
    reference = request.GET.get('reference')
    trxref = request.GET.get('trxref')
    
    if not reference:
        return error_response("Reference not found in the request.")

    if reference == trxref:
        data = verify_payment(reference)
        
        if data['status'] == 'success':
            customer_email = data['customer']['email']
            amount_paid = data['amount'] 
            paid_at = data['paidAt']
            status = data['status']
            
           
                
            response_message = (
                f"Payment successful! <br>"
                f"Customer Email: {customer_email} <br>"
                f"Amount Paid: {amount_paid} NGN <br>"
                f"Paid At: {paid_at} <br>"
                f"Status: {status}"
            )
            
            return HttpResponse(response_message)
        else:
            return error_response("Payment verification failed.")
    else:
        return error_response("Reference and trxref do not match.")



@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
def paystack_webhook(request):
    event = request.data
    if event['event'] == 'charge.success':
        return success_response()
    return error_response("Invalid event")




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
