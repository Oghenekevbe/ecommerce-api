from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.functions import Lower
from django.db import transaction

# Django REST Framework imports
from rest_framework import generics, mixins, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

# DRF-YASG (Swagger) imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# PostgreSQL-specific optimization
from django.contrib.postgres.search import SearchVector

# Local application imports
from .models import Product, Review, BillingAddress, Cart, CartItem
from .serializers import (
    ProductSerializer, ReviewSerializer, BillingAddressSerializer, 
    CartItemSerializer, CartSerializer, ProductListSerializer
)
from services.service_responses import (
    success_response, created_response, error_response, 
    accepted_response, no_content_response
)


User = get_user_model()





#PRODUCT SEARCH, VIEW AND REVIEW

class ProductSearch(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        query_type = request.GET.get("query_type")
        query_value = request.GET.get("query_value")

        if not query_type or not query_value:
            return error_response("Missing or empty query parameters")

        cache_key = f"search_{query_type}_{query_value}"
        cached_products = cache.get(cache_key)

        if cached_products:
            print("Fetching search results from cache...")
            products = cached_products
        else:
            print("Fetching search results from database...")

            if query_type == "product":
                products = Product.objects.annotate(search=SearchVector("name")).filter(search=query_value)

            elif query_type == "category":
                products = Product.objects.filter(
                    category__name__icontains=query_value
                ).select_related("category").annotate(
                    lower_name=Lower("category__name")
                ).order_by("lower_name")  # Optimized with trigram indexes

            elif query_type == "availability":
                products = Product.objects.filter(is_available=True)  # Indexed field

            else:
                return error_response("Invalid query_type parameter")

            cache.set(cache_key, products, timeout=300)  # Cache for 5 minutes

        # Paginate the queryset
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)

        if paginated_products is not None:
            serializer = self.serializer_class(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Fallback if pagination is not applied
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductView(ListAPIView):
    print("cache class: ", cache.__class__)
    
    def get_serializer_class(self):
        if self.kwargs.get("pk"):
            return ProductSerializer  # Detailed view
        return ProductListSerializer  # List view

    def get_queryset(self):
        return Product.objects.select_related("category", "seller", "promo").all().order_by("name")

    @swagger_auto_schema(
        responses={
            200: openapi.Response("List of products or product details", ProductSerializer(many=True)),
            404: openapi.Response("Product not found"),
        },
        operation_summary="Retrieve all products or a specific product by ID",
        tags=["Products"],
    )
    def get(self, request, pk=None):
        if pk:
            cache_key = f"product_{pk}"
            product = cache.get(cache_key)
            
            if product:
                print("Fetching product from cache...")
            else:
                print("Fetching product from database...")
                product = get_object_or_404(self.get_queryset(), pk=pk)
                cache.set(cache_key, product, timeout=300)  # Cache for 5 minutes
            
            serializer = self.get_serializer_class()(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        cache_key = "all_products"
        queryset = cache.get(cache_key)
        if queryset:
            print("Fetching all products from cache...")
        else:
            print("Fetching all products from database...")
            queryset = self.get_queryset()
            cache.set(cache_key, queryset, timeout=300)  # Cache for 5 minutes
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer_class()(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewView(generics.GenericAPIView):
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the product"),
                "user": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the user"),
                "rating": openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating"),
                "comment": openapi.Schema(type=openapi.TYPE_STRING, description="Review comment"),
            },
            required=["product", "user", "rating"],
        ),
        responses={
            201: openapi.Response("Review successfully created", ReviewSerializer),
            400: "Invalid input data",
        },
        operation_summary="Create a product review",
        tags=["Reviews"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return created_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("List of reviews for a product", ReviewSerializer(many=True)),
        },
        operation_summary="List reviews for a specific product",
        tags=["Reviews"],
    )
    def get(self, request, product_id=None, review_id=None):
        if review_id:
            # Retrieve and return details of a specific review
            review = get_object_or_404(Review, id=review_id)
            serializer = self.serializer_class(instance=review)
            return success_response(serializer.data)
        elif product_id:
            # Retrieve and return all reviews for a specific product
            reviews = Review.objects.filter(product_id=product_id)
            serializer = self.serializer_class(instance=reviews, many=True)
            return success_response(serializer.data)
        else:
            return error_response({"detail": "Product ID or Review ID must be provided."})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "rating": openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating"),
                "comment": openapi.Schema(type=openapi.TYPE_STRING, description="Review comment"),
            },
        ),
        responses={
            200: openapi.Response("Review successfully updated", ReviewSerializer),
            400: "Invalid input data",
            404: "Review not found",
        },
        operation_summary="Update a specific review",
        tags=["Reviews"],
    )
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = self.serializer_class(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        responses={
            204: "Review successfully deleted",
            404: "Review not found",
        },
        operation_summary="Delete a specific review",
        tags=["Reviews"],
    )
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return no_content_response()



#CART VIEW CART ITEM VIEW(VIEW ALL ITEMS, ADD TO CART, UPDATE CART ITEMS AND DELETE CART ITEMS) 

class CartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Cart details", CartSerializer),
            404: "Cart not found",
        },
        tags=["Store"],
        operation_summary="Get the cart and all the items in it",
    )
    def get(self, request):
        cache_key = f"cart_{request.user.id}" #it has to be unique to all users
        cached_cart = cache.get(cache_key)
        if cached_cart:
            print('fetching cached cart')
            order = cached_cart
        else:
            user = request.user
            order, created = Cart.objects.get_or_create(user=user, is_active=True)
            serializer = self.serializer_class(order)
            cache.set(cache_key, serializer.data, timeout=300)
            return success_response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "address": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            202: openapi.Response("Cart updated successfully", CartSerializer),
            400: "Invalid input data",
        },
        tags=["Store"],
        operation_summary="Update the cart address",
    )
    def put(self, request):
        cache_key = f"cart_{request.user.id}" 
        user = request.user
        order = get_object_or_404(Cart, user=user, is_active=True)  # Ensure we update only the active cart
        serializer = self.serializer_class(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            cache.set(cache_key, serializer.data, timeout=300)
            return accepted_response(serializer.data)
        
        return error_response(serializer.errors)

class CartItemView(generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict queryset to only the cart items of the authenticated user."""
        user = self.request.user
        return CartItem.objects.filter(order__user=user)

    @swagger_auto_schema(
        tags=["Store"],
        operation_summary="Retrieve cart items for the current user",
        operation_description="This endpoint retrieves the cart items for the current user.",
        responses={status.HTTP_200_OK: CartItemSerializer(many=True)},
    )
    def get(self, request, pk=None):
        user = request.user

        if pk is not None:
            # Retrieve a specific cart item
            cart_item = get_object_or_404(CartItem, id=pk, order__user=user)
            serializer = self.serializer_class(cart_item)
            return success_response(serializer.data)

        # Retrieve all cart items for the user
        order, created = Cart.objects.get_or_create(user=user, is_active=True)
        cart_items = order.cart_items.all()
        serializer = self.serializer_class(cart_items, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        tags=["Store"],
        operation_summary="Add a product to the cart",
        operation_description="This endpoint adds a product to the user's cart.",
        request_body=CartItemSerializer,
        responses={
            status.HTTP_201_CREATED: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            with transaction.atomic():
                cart_item = serializer.save() 
            return created_response(CartItemSerializer(cart_item).data)

        return error_response(serializer.errors)

    @swagger_auto_schema(
        tags=["Store"],
        operation_summary="Update a specific cart item",
        request_body=CartItemSerializer,
        responses={
            status.HTTP_202_ACCEPTED: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Cart item not found",
        },
    )
    def put(self, request, pk):
        user = request.user
        cart_item = get_object_or_404(CartItem, id=pk, order__user=user)  # Ensure the item belongs to the user
        data = request.data
        serializer = self.serializer_class(cart_item, data=data, partial=True)

        if serializer.is_valid():
            seller = cart_item.product.seller  # Get seller directly from the related product
            
            if user == seller.user:  # Ensure you're comparing with seller's user
                return error_response("You cannot transact with your own product")
            
            with transaction.atomic():
                serializer.save()
            return accepted_response(serializer.data)

        return error_response(serializer.errors)
    @swagger_auto_schema(
        tags=["Store"],
        operation_summary="Delete a specific cart item",
        responses={
            status.HTTP_204_NO_CONTENT: "Cart item deleted successfully",
            status.HTTP_404_NOT_FOUND: "Cart item not found",
        },
    )
    def delete(self, request, pk):
        user = request.user
        cart_item = get_object_or_404(CartItem, id=pk, order__user=user)  # Restrict deletion to user's own cart
        cart_item.delete()
        return no_content_response()






class CartHistory(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Store"],
        operation_summary="Get inactive carts for order history",
        responses={
            status.HTTP_200_OK: CartSerializer(many=True),
        },
    )
    def get(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user, is_active=False)
        serializer = self.serializer_class(carts, many=True)
        return success_response(serializer.data)



#BILLING ADRESS VIEW
class BillingAddressListCreateAPIView(generics.ListCreateAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer

    @swagger_auto_schema(
        operation_summary="List or create billing addresses",
        responses={
            200: BillingAddressSerializer(many=True),
            201: BillingAddressSerializer,
            400: "Invalid input data",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BillingAddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve, update, or delete a billing address",
        responses={
            200: BillingAddressSerializer,
            204: "Billing address successfully deleted",
            400: "Invalid input data",
            404: "Billing address not found",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


