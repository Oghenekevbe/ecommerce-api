# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status, generics, permissions
# from rest_framework.views import APIView
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from .models import (
#     Product,
#     Review,
#     BillingAddress,
#     Cart,
#     CartItem,
# )
# from .serializers import (
#     ProductSerializer,
#     ReviewSerializer,
#     BillingAddressSerializer,
#     CartItemSerializer,
#     CartSerializer,
# )
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ProductSearch(APIView):
#     serializer_class = ProductSerializer

#     def get(self, request):
#         query_type = request.GET.get("query_type")
#         query_value = request.GET.get("query_value")

#         if query_type and query_value:
#             if query_type == "product":
#                 products = Product.objects.filter(name__icontains=query_value)
#             elif query_type == "category":
#                 products = Product.objects.filter(category__name__icontains=query_value)
#             else:
#                 return Response(
#                     {"error": "Invalid query_type parameter"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             serializer = self.serializer_class(products, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)

#         return Response(
#             {"error": "Missing or empty query parameters"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# class ProductListView(APIView):
#     serializer_class = ProductSerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response("List of products", ProductSerializer(many=True)),
#         },
#         operation_summary="Get a list of all products",
#         tags=["Products"],
#     )
#     def get(self, request, *args, **kwargs):
#         """
#         Get a list of products.
#         """
#         products = Product.objects.all()
#         serializer = self.serializer_class(instance=products, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class ProductDetailView(APIView):
#     serializer_class = ProductSerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response("Details of a product", ProductSerializer),
#             404: "Product not found",
#         },
#         operation_summary="Get details of a specific product",
#         tags=["Products"],
#     )
#     def get(self, request, pk):
#         """
#         Get details of a specific product.
#         """
#         product = get_object_or_404(Product, pk=pk)
#         serializer = self.serializer_class(instance=product)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)




# """
# REVIEW APIS
# """


# class ReviewCreateView(APIView):
#     serializer_class = ReviewSerializer

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "product": openapi.Schema(
#                     type=openapi.TYPE_INTEGER, description="ID of the product"
#                 ),
#                 "user": openapi.Schema(
#                     type=openapi.TYPE_INTEGER, description="ID of the user"
#                 ),
#                 "rating": openapi.Schema(
#                     type=openapi.TYPE_INTEGER, description="Rating"
#                 ),
#                 "comment": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Review comment"
#                 ),
#             },
#             required=["product", "user", "rating"],
#         ),
#         operation_summary="Create a product review",
#         responses={
#             201: openapi.Response("Review successfully created", ReviewSerializer),
#             400: "Invalid input data",
#         },
#         tags=["Reviews"],
#     )
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReviewListView(APIView):
#     serializer_class = ReviewSerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response(
#                 "List of reviews for a product", ReviewSerializer(many=True)
#             ),
#         },
#         tags=["Reviews"],
#         operation_summary="List of reviews for a specific product",
#     )
#     def get(self, request, product_id):
#         reviews = self.get_reviews(product_id)
#         serializer = self.serializer_class(instance=reviews, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def get_reviews(self, product_id):
#         """
#         Helper function to retrieve reviews for a product.
#         """
#         return Review.objects.filter(product_id=product_id)


# class ReviewDetailView(APIView):
#     serializer_class = ReviewSerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response("Details of a review", ReviewSerializer),
#             404: "Review not found",
#         },
#         tags=["Reviews"],
#         operation_summary="Details for a specific review",
#     )
#     def get(self, request, review_id):
#         review = get_object_or_404(Review, id=review_id)
#         serializer = self.serializer_class(instance=review)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ReviewUpdateView(APIView):
#     serializer_class = ReviewSerializer

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "rating": openapi.Schema(
#                     type=openapi.TYPE_INTEGER, description="Rating"
#                 ),
#                 "comment": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Review comment"
#                 ),
#             },
#         ),
#         responses={
#             200: openapi.Response("Review successfully updated", ReviewSerializer),
#             400: "Invalid input data",
#             404: "Review not found",
#         },
#         tags=["Reviews"],
#         operation_summary="Update a specific review",
#     )
#     def put(self, request, review_id):
#         review = get_object_or_404(Review, id=review_id)
#         serializer = self.serializer_class(instance=review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReviewDeleteView(APIView):
#     @swagger_auto_schema(
#         responses={
#             204: "Review successfully deleted",
#             404: "Review not found",
#         },
#         tags=["Reviews"],
#         operation_summary="Delete a specific review",
#     )
#     def delete(self, request, review_id):
#         review = get_object_or_404(Review, id=review_id)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)






# """CART APIS"""


# class CartView(APIView):

#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response("Cart details", CartSerializer),
#             404: "Cart not found",
#         },
#         tags=["Cart"],
#         operation_summary="Get the cart and all the items in it",
#     )
#     def get(self, request):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_active=True)
#         serializer = self.serializer_class(order)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "key": openapi.Schema(type=openapi.TYPE_STRING),
#                 "value": openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         responses={
#             202: openapi.Response("Cart updated successfully", CartSerializer),
#             400: "Invalid input data",
#         },
#         tags=["Cart"],
#         operation_summary="Update the cart address",
#     )
#     def put(self, request):
#         user = request.user
#         order = get_object_or_404(Cart, user=user)
#         serializer = self.serializer_class(order, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddToCartView(APIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         tags=["Cart"],
#         operation_summary="Retrieve cart items for the current user",
#         operation_description="This endpoint retrieves the cart items for the current user.",
#         responses={status.HTTP_200_OK: CartItemSerializer(many=True)},
#     )
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_actve=True)
#         cart_items = order.cart_items.all()
#         serializer = self.serializer_class(cart_items, many=True)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["Cart"],
#         operation_summary="Add a product to the cart",
#         operation_description="This endpoint adds a product to the user's cart.",
#         request_body=CartItemSerializer,
#         responses={
#             status.HTTP_201_CREATED: CartItemSerializer,
#             status.HTTP_400_BAD_REQUEST: "Bad Request",
#         },
#     )
#     def post(self, request):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_actve=True)
#         serializer = self.serializer_class(
#             data=request.data,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateCartItem(APIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="Retrieve details of a specific cart item",
#         operation_description="This endpoint returns details of a cart item identified by its primary key.",
#         responses={status.HTTP_200_OK: CartItemSerializer},
#         tags=["Cart"],
#     )
#     def get(self, request, pk):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_actve=True)
#         cart_item = get_object_or_404(CartItem, order=order, pk=pk)
#         serializer = self.serializer_class(cart_item)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         operation_summary="Update a specific cart item",
#         operation_description="This endpoint updates the details of a specific cart item identified by its primary key.",
#         request_body=CartItemSerializer,
#         responses={
#             status.HTTP_202_ACCEPTED: CartItemSerializer,
#             status.HTTP_400_BAD_REQUEST: "Bad Request",
#         },
#         tags=["Cart"],
#     )
#     def put(self, request, pk):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_actve=True)
#         cart_item = get_object_or_404(CartItem, order=order, pk=pk)
#         serializer = self.serializer_class(cart_item, data=request.data)
#         if serializer.is_valid():
#             serializer.save(partial=True)
#             return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeleteCartItem(APIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="Retrieve details of a specific cart item",
#         operation_description="This endpoint returns details of a cart item identified by its primary key.",
#         responses={status.HTTP_200_OK: CartItemSerializer},
#         tags=["Cart"],
#     )
#     def get(self, request, pk):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_actve=True)
#         cart_item = get_object_or_404(CartItem, order=order, pk=pk)
#         serializer = self.serializer_class(cart_item)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         operation_summary="Delete a specific cart item",
#         operation_description="This endpoint deletes a specific cart item identified by its primary key.",
#         responses={status.HTTP_204_NO_CONTENT: "Cart item successfully deleted"},
#         tags=["Cart"],
#     )
#     def delete(self, request, pk):
#         user = request.user
#         order, created = Cart.objects.get_or_create(user=user, is_actve=True)
#         cart_item = get_object_or_404(CartItem, order=order, pk=pk)
#         cart_item.delete()
#         response = {"message": "Cart item successfully deleted"}
#         return Response(data=response, status=status.HTTP_204_NO_CONTENT)


# class cartHistory(APIView):
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         orders = Cart.objects.filter(user=user, is_active=False)
#         seriializer = self.serializer_class(orders, many=True)

#         return Response(data=seriializer.data, status=status.HTTP_200_OK)


# """ADDRESS API"""


# class BillingAddressListCreateAPIView(generics.ListCreateAPIView):
#     queryset = BillingAddress.objects.all()
#     serializer_class = BillingAddressSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_description="List all billing addresses or create a new one.",
#         responses={200: BillingAddressSerializer(many=True)},
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     @swagger_auto_schema(
#         operation_description="Create a new billing address.",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "address": openapi.Schema(type=openapi.TYPE_STRING),
#                 "city": openapi.Schema(type=openapi.TYPE_STRING),
#                 "state": openapi.Schema(type=openapi.TYPE_STRING),
#                 "zipcode": openapi.Schema(type=openapi.TYPE_STRING),
#                 "is_billing_address": openapi.Schema(type=openapi.TYPE_BOOLEAN),
#             },
#         ),
#         responses={201: BillingAddressSerializer()},
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)


# class BillingAddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BillingAddress.objects.all()
#     serializer_class = BillingAddressSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_description="Retrieve a billing address by ID.",
#         responses={200: BillingAddressSerializer()},
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     @swagger_auto_schema(
#         operation_description="Update a billing address by ID.",
#         request_body=BillingAddressSerializer,
#         responses={200: BillingAddressSerializer()},
#     )
#     def put(self, request, *args, **kwargs):
#         return super().put(request, *args, **kwargs)

#     @swagger_auto_schema(
#         operation_description="Delete a billing address by ID.", responses={204: None}
#     )
#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)




from services import service_responses as sr
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Review, BillingAddress, Cart, CartItem
from .serializers import ProductSerializer, ReviewSerializer, BillingAddressSerializer, CartItemSerializer, CartSerializer
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class ProductSearch(generics.GenericApiView):
    serializer_class = ProductSerializer

    def get(self, request):
        query_type = request.GET.get("query_type")
        query_value = request.GET.get("query_value")

        if query_type and query_value:
            if query_type == "product":
                products = Product.objects.filter(name__icontains=query_value)
            elif query_type == "category":
                products = Product.objects.filter(category__name__icontains=query_value)
            else:
                return sr.error_response("Invalid query_type parameter")

            serializer = self.serializer_class(products, many=True)
            return sr.success_response(serializer.data)

        return sr.error_response("Missing or empty query parameters")

class ProductView(generics.GenericApiView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response("List of products", ProductSerializer(many=True)),
            404: "Product not found",
        },
        operation_summary="Get a list of all products or details of a specific product",
        tags=["Products"],
    )
    def get(self, request, pk=None):
        if pk:
            # Retrieve and return details of a specific product
            product = get_object_or_404(Product, pk=pk)
            serializer = self.serializer_class(instance=product)
            return sr.success_response(serializer.data)
        else:
            # Retrieve and return all products
            products = Product.objects.all()
            serializer = self.serializer_class(instance=products, many=True)
            return sr.success_response(serializer.data)

class ReviewView(generics.GenericApiView):
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
            return sr.created_response(serializer.data)
        return sr.error_response(serializer.errors)

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
            return sr.success_response(serializer.data)
        elif product_id:
            # Retrieve and return all reviews for a specific product
            reviews = Review.objects.filter(product_id=product_id)
            serializer = self.serializer_class(instance=reviews, many=True)
            return sr.success_response(serializer.data)
        else:
            return sr.error_response({"detail": "Product ID or Review ID must be provided."})

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
            return sr.success_response(serializer.data)
        return sr.error_response(serializer.errors)

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
        return sr.no_content_response()


class CartView(generics.GenericApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Cart details", CartSerializer),
            404: "Cart not found",
        },
        tags=["Cart"],
        operation_summary="Get the cart and all the items in it",
    )
    def get(self, request):
        user = request.user
        order, created = Cart.objects.get_or_create(user=user, is_active=True)
        serializer = self.serializer_class(order)
        return sr.success_response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "key": openapi.Schema(type=openapi.TYPE_STRING),
                "value": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            202: openapi.Response("Cart updated successfully", CartSerializer),
            400: "Invalid input data",
        },
        tags=["Cart"],
        operation_summary="Update the cart address",
    )
    def put(self, request):
        user = request.user
        order = get_object_or_404(Cart, user=user)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return sr.accepted_response(serializer.data)
        return sr.error_response(serializer.errors)

class CartItemView(generics.GenericApiView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Cart"],
        operation_summary="Retrieve cart items for the current user",
        operation_description="This endpoint retrieves the cart items for the current user.",
        responses={status.HTTP_200_OK: CartItemSerializer(many=True)},
    )
    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            # Retrieve a specific cart item
            cart_item = get_object_or_404(CartItem, pk=pk)
            serializer = self.serializer_class(cart_item)
            return sr.success_response(serializer.data)
        else:
            # Retrieve all cart items for the user
            order, created = Cart.objects.get_or_create(user=user, is_active=True)
            cart_items = order.cart_items.all()
            serializer = self.serializer_class(cart_items, many=True)
            return sr.success_response(serializer.data)

    @swagger_auto_schema(
        tags=["Cart"],
        operation_summary="Add a product to the cart",
        operation_description="This endpoint adds a product to the user's cart.",
        request_body=CartItemSerializer,
        responses={
            status.HTTP_201_CREATED: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
    )
    def post(self, request):
        user = request.user
        order, created = Cart.objects.get_or_create(user=user, is_active=True)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item = serializer.save(cart=order)
            return sr.created_response(CartItemSerializer(item).data)
        return sr.error_response(serializer.errors)

    @swagger_auto_schema(
        tags=["Cart"],
        operation_summary="Update a specific cart item",
        request_body=CartItemSerializer,
        responses={
            status.HTTP_202_ACCEPTED: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Cart item not found",
        },
    )
    def put(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        serializer = self.serializer_class(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return sr.accepted_response(serializer.data)
        return sr.error_response(serializer.errors)

    @swagger_auto_schema(
        tags=["Cart"],
        operation_summary="Delete a specific cart item",
        responses={
            status.HTTP_204_NO_CONTENT: "Cart item deleted successfully",
            status.HTTP_404_NOT_FOUND: "Cart item not found",
        },
    )
    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return sr.no_content_response()
    
class CartHistory(generics.GenericApiView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Cart"],
        operation_summary="Get inactive carts for order history",
        responses={
            status.HTTP_200_OK: CartSerializer(many=True),
        },
    )
    def get(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user, is_active=False)
        serializer = self.serializer_class(carts, many=True)
        return sr.success_response(serializer.data)

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


