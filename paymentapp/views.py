from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.decorators import APIView
from store.models import Cart, CartItem
from store.serializers import CartSerializer, CartItemSerializer

# Create your views here.


class makePayment(APIView):
    permission_classes = [permissions.IsAuthenticated]


class orderCompletedView(APIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            order = Cart.objects.get(user=user, is_active=True)
            order.status = "confirmed"
            order.save()
            order.is_active = False  # Set the cart as inactive
            order.save()
        except Cart.DoesNotExist:
            pass

        # Create a new empty cart for the user
        new_order = Cart.objects.create(user=user)
        new_order.save()
        response = {"message": "Payment Successful"}
        return Response(data=response, status=status.HTTP_200_OK)
