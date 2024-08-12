from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from services import service_responses as sr
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from store.models import (Product,BillingAddress,Cart,CartItem, Promotion)
from storeSellers.models import Seller
from storeAdmin.serializers import SellerSerializer
from store.models import Category

from .permissions import IsStaffMixin, IsAdminMixin
from .serializers import CategorySerializer
from store.serializers import (ProductSerializer,BillingAddressSerializer,CartItemSerializer,CartSerializer,PromotionSerializer,)
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model


# ADMIN VIEWS

User = get_user_model()


"""
CATEGORY APIS
"""


# class CategoryCreateView(APIView):
#     serializer_class = CategorySerializer

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "name": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Name of the category"
#                 ),
#                 "description": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Description of the category"
#                 ),
#             },
#             required=["name"],
#         ),
#         responses={
#             201: openapi.Response("Category successfully created", CategorySerializer),
#             400: "Invalid input data",
#         },
#         tags=["Categories"],
#         operation_summary="Create a category",
#     )
#     def post(self, request):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message": "Category successfully created",
#                 "data": serializer.data,
#             }
#             return Response(data=response, status=status.HTTP_201_CREATED)

#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryListView(APIView):
#     serializer_class = CategorySerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response("List of categories", CategorySerializer(many=True)),
#         },
#         tags=["Categories"],
#         operation_summary="Get a list of all categories",
#     )
#     def get(self, request, *args, **kwargs):
#         categories = Category.objects.all()
#         serializer = self.serializer_class(instance=categories, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class CategoryDetailView(APIView):
#     serializer_class = CategorySerializer

#     @swagger_auto_schema(
#         responses={
#             200: openapi.Response("Details of a category", CategorySerializer),
#             404: "Category not found",
#         },
#         tags=["Categories"],
#         operation_summary="Get details of a specific category",
#     )
#     def get(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = self.serializer_class(instance=category)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class CategoryUpdateView(APIView, IsStaffMixin, IsAdminMixin):
#     serializer_class = CategorySerializer

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "name": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Updated name of the category"
#                 ),
#                 "description": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Updated description"
#                 ),
#             },
#         ),
#         responses={
#             200: openapi.Response("Category successfully updated", CategorySerializer),
#             400: "Invalid input data",
#             404: "Category not found",
#         },
#         tags=["Categories"],
#         operation_summary="Update a specific category",
#     )
#     def put(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         data = request.data
#         serializer = self.serializer_class(instance=category, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message": "Category successfully updated",
#                 "data": serializer.data,
#             }
#             return Response(data=response, status=status.HTTP_200_OK)

#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryDeleteView(APIView, IsStaffMixin, IsAdminMixin):
#     @swagger_auto_schema(
#         responses={
#             204: "Category successfully deleted",
#             404: "Category not found",
#         },
#         tags=["Categories"],
#         operation_summary="Delete a specific category",
#     )
#     def delete(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         category.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the category"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Description of the category"
                ),
            },
            required=["name"],
        ),
        responses={
            201: openapi.Response("Category successfully created", CategorySerializer),
            400: "Invalid input data",
        },
        tags=["Categories"],
        operation_summary="Create a category",
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return sr.created_response(serializer.data, status.HTTP_201_CREATED)
        
        return sr.error_response(serializer.errors)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("List of categories", CategorySerializer(many=True)),
        },
        tags=["Categories"],
        operation_summary="Get a list of all categories",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView, IsStaffMixin, IsAdminMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Details of a category", CategorySerializer),
            404: "Category not found",
        },
        tags=["Categories"],
        operation_summary="Get details of a specific category",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Updated name of the category"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Updated description"
                ),
            },
        ),
        responses={
            200: openapi.Response("Category successfully updated", CategorySerializer),
            400: "Invalid input data",
            404: "Category not found",
        },
        tags=["Categories"],
        operation_summary="Update a specific category",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: "Category successfully deleted",
            404: "Category not found",
        },
        tags=["Categories"],
        operation_summary="Delete a specific category",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# class OrdersView(APIView, IsStaffMixin, IsAdminMixin):
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="Retrieve details of all orders by customers",
#         operation_description="This endpoint returns details of orders.",
#         responses={status.HTTP_200_OK: CartItemSerializer},
#         tags=["Cart"],
#     )
#     def get(self, request):
#         orders = Cart.objects.all()
#         serializer = self.serializer_class(orders, many=True)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class OrderDetailView(APIView, IsStaffMixin, IsAdminMixin):
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="Retrieve details of specific orders by customers",
#         operation_description="This endpoint returns details of specific orders for the admin.",
#         responses={status.HTTP_200_OK: CartItemSerializer},
#         tags=["Cart"],
#     )
#     def get(self, request, pk):
#         order = get_object_or_404(Cart, pk=pk)
#         serializer = self.serializer_class(order)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class AdminOrderUpdateDeleteView(APIView, IsAdminMixin):
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="Retrieve details of specific orders by customers",
#         operation_description="This endpoint returns details of specific orders for the admin.",
#         responses={status.HTTP_200_OK: CartItemSerializer},
#         tags=["Cart"],
#     )
#     def put(self, request, pk):
#         data = request.data
#         order = get_object_or_404(Cart, pk=pk)
#         serializer = self.serializer_class(data, order)
#         if serializer.is_valid():
#             serializer.save()

#             return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderView(generics.GenericAPIView, IsStaffMixin, IsAdminMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve orders",
        operation_description="Lists all orders or retrieves a specific order.",
        responses={
            status.HTTP_200_OK: CartSerializer(many=True),
            status.HTTP_404_NOT_FOUND: "Order not found"
        },
        tags=["Cart"],
    )
    def get(self, request, pk=None):
        if pk:
            # Retrieve a specific order
            order = get_object_or_404(Cart, pk=pk)
            serializer = self.serializer_class(order)
            return sr.success_response(serializer.data)
        else:
            # List all orders
            orders = Cart.objects.all()
            serializer = self.serializer_class(orders, many=True)
            return sr.success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update or delete a specific order",
        operation_description="Allows updating or deleting a specific order.",
        responses={
            status.HTTP_202_ACCEPTED: CartSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid input data",
            status.HTTP_404_NOT_FOUND: "Order not found",
        },
        tags=["Cart"],
    )
    def put(self, request, pk):
        order = get_object_or_404(Cart, pk=pk)
        serializer = self.serializer_class(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return sr.accepted_response(serializer.data)
        return sr.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = get_object_or_404(Cart, pk=pk)
        order.delete()
        return sr.no_content_response()

class AdminUpdateDeleteCartItem(APIView, IsAdminMixin):
    serializer_class = CartItemSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific cart item",
        operation_description="This endpoint returns details of a cart item identified by its primary key.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        tags=["Cart"],
    )
    def get(self, request, cart_pk, pk):
        order = get_object_or_404(Cart, pk=cart_pk)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item)
        return sr.success_response(data=serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a specific cart item",
        operation_description="This endpoint updates the details of a specific cart item identified by its primary key.",
        request_body=CartItemSerializer,
        responses={
            status.HTTP_200_OK: CartItemSerializer,
            status.HTTP_204_NO_CONTENT: "Cart item successfully deleted",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
        },
        tags=["Cart"],
    )
    def put(self, request, cart_pk, pk):
        order = get_object_or_404(Cart, pk=cart_pk)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return sr.success_response(serializer.data, status.HTTP_200_OK)
        return sr.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a specific cart item",
        operation_description="This endpoint deletes a specific cart item identified by its primary key.",
        responses={
            status.HTTP_204_NO_CONTENT: sr.no_content_response(),
            status.HTTP_404_NOT_FOUND: sr.error_response("Cart or Cart item not found"),
        },
        tags=["Cart"],
    )
    def delete(self, request, cart_pk, pk):
        order = get_object_or_404(Cart, pk=cart_pk)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        cart_item.delete()
        return sr.no_content_response()


class PromotionListCreateAPIView(generics.ListCreateAPIView, IsAdminMixin):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="List Promotions",
        operation_description="Get a list of all promotions.",
        responses={200: PromotionSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Create Promotion",
        operation_description="Create a new promotion.",
        request_body=PromotionSerializer,
        responses={201: PromotionSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PromotionRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView, IsAdminMixin
):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Retrieve Promotion",
        operation_description="Retrieve details of a specific promotion.",
        responses={200: PromotionSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Update Promotion",
        operation_description="Update details of a specific promotion.",
        request_body=PromotionSerializer,
        responses={200: PromotionSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Delete Promotion",
        operation_description="Delete a specific promotion.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductListCreateAPIView(generics.ListCreateAPIView, IsAdminMixin):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set the 'created_by' field to the current user when creating a new product
        serializer.save(created_by=request.user)
        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView, IsAdminMixin
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a product",
        operation_description="This endpoint retrieves details of a specific product.",
        responses={200: ProductSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a product",
        operation_description="This endpoint updates details of a specific product.",
        request_body=ProductSerializer,
        responses={200: ProductSerializer()},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Set the 'updated_by' field to the current user when updating a product
        serializer.save(updated_by=request.user)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update a product",
        operation_description="This endpoint partially updates details of a specific product.",
        request_body=ProductSerializer,
        responses={200: ProductSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a product",
        operation_description="This endpoint deletes a specific product.",
        responses={204: "No Content"},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class SellerListCreateView(generics.ListCreateAPIView, IsAdminMixin, IsStaffMixin):
    """
    get:
    Return a list of all sellers.

    post:
    Create a new seller.
    """

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("List of Sellers", SellerSerializer(many=True)),
            201: openapi.Response("Created Seller", SellerSerializer),
        },
        tags=["Sellers"],
        operation_summary="Get a list of all sellers",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "company_name": openapi.Schema(type=openapi.TYPE_STRING),
                "address": openapi.Schema(type=openapi.TYPE_STRING),
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["company_name", "address", "phone_number"],
        ),
        responses={
            201: openapi.Response("Created Seller", SellerSerializer),
        },
        tags=["Sellers"],
        operation_summary="Create a seller",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SellerRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView, IsAdminMixin, IsStaffMixin
):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Details of a seller", SellerSerializer),
            404: "Seller not found",
        },
        tags=["Sellers"],
        operation_summary="Update details of a specific  seller",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "company_name": openapi.Schema(type=openapi.TYPE_STRING),
                "address": openapi.Schema(type=openapi.TYPE_STRING),
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["company_name"],  # Specify required properties here
        ),
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Details of a seller", SellerSerializer),
            204: "No Content",
            404: "Seller not found",
        },
        tags=["Sellers"],
        operation_summary="Delete a seller",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserProfileView(APIView, IsStaffMixin):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        operation_summary="Get user profile",
        operation_description="Get the profile of the authenticated user.",
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AdminUserBillingAddressesAPIView(generics.ListAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all billing addresses for all users and specific user by user ID.",
        responses={200: BillingAddressSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class AdmincartHistory(APIView, IsStaffMixin):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = User(pk=pk)
        if user:
            orders = Cart.objects.filter(user=user, is_active=False)
            if orders:
                seriializer = self.serializer_class(orders, many=True)
                return Response(data=seriializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={
                        "message": "Error! There is presently no order history for this user"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
