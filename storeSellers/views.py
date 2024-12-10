from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import  Seller
from store.models import Product, CartItem


from .permissions import IsSellerMixin
from store.serializers import (
    ProductSerializer, CartItemSerializer
)
from services import service_responses as sr




"""SELLER APIS"""


class ProductCreateView(generics.ListCreateAPIView, IsSellerMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List products",
        operation_description="This endpoint retrieves a list of products.",
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product",
        operation_description="This endpoint creates a new product.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer()},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        seller = Seller.objects.get(user=user)
        serializer = self.get_serializer(seller, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set the 'created_by' field to the current user when creating a new product
        serializer.save(created_by=request.user)
        return super().create(request, *args, **kwargs)


class SellerOrdersAPIView(generics.GenericAPIView, IsSellerMixin):
    @swagger_auto_schema(
        tags=["Seller"],
        operation_summary="Get Seller Orders",
        operation_description="Get all orders associated with the authenticated seller.",
        responses={200: CartItemSerializer(many=True)},
    )
    def get(self, request):
        # Assuming the seller is authenticated and available in the request
        seller = request.user.seller
        seller_orders = CartItem.objects.filter(product__seller=seller).distinct()
        serializer = CartItemSerializer(seller_orders, many=True)
        return sr.accepted_response(data=serializer.data)


