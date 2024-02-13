from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Category, Review,BillingAddress,Cart,CartItem,Seller, Promotion
from .permissions import IsSellerMixin,IsStaffMixin,IsAdminMixin
from .serializers import ProductSerializer, ReviewSerializer, CategorySerializer,SellerSerializer,BillingAddressSerializer,CartItemSerializer,CartSerializer, PromotionSerializer
from user.serializers import UserSerializer






class ProductSearch(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        query_type = request.GET.get('query_type')
        query_value = request.GET.get('query_value')

        if query_type and query_value:
            if query_type == 'product':
                products = Product.objects.filter(name__icontains=query_value)
            elif query_type == 'category':
                products = Product.objects.filter(category__name__icontains=query_value)
            else:
                return Response({"error": "Invalid query_type parameter"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(products, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Missing or empty query parameters"}, status=status.HTTP_400_BAD_REQUEST)


        

class ProductListView(APIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of products', ProductSerializer(many=True)),
        },
        operation_summary = 'Get a list of all products',
        tags=['Products'],
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of products.
        """
        products = Product.objects.all()
        serializer = self.serializer_class(instance=products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Details of a product', ProductSerializer),
            404: 'Product not found',
        },
        operation_summary = 'Get details of a specific product',
        tags=['Products'],
    )
    def get(self, request, pk):
        """
        Get details of a specific product.
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(instance=product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductUpdateView(APIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Updated name of the product'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Updated description'),
                # ... other properties ...
            },
        ),
        responses={
            200: openapi.Response('Product successfully updated', ProductSerializer),
            400: 'Invalid input data',
            404: 'Product not found',
        },
        tags=['Products'],
        operation_summary = 'Update details of a specific product',
    )
    def put(self, request, pk):
        """
        Update a specific product.
        """
        product = get_object_or_404(Product, pk=pk)
        data = request.data
        serializer = self.serializer_class(instance=product, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Product successfully updated',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    @swagger_auto_schema(
        responses={
            204: 'Product successfully deleted',
            404: 'Product not found',
        },
        tags=['Products'],
        operation_summary = 'Delete a specific product',
    )
    def delete(self, request, pk):
        """
        Delete a specific product.
        """
        product = get_object_or_404(Product, pk=pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

'''
REVIEW APIS
'''


class ReviewCreateView(APIView):
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product'),
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user'),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating'),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Review comment'),
            },
            required=['product', 'user', 'rating'],
        ),
        operation_summary = 'Create a product review',
        responses={
            201: openapi.Response('Review successfully created', ReviewSerializer),
            400: 'Invalid input data',
        },
        tags=['Reviews'],
        
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewListView(APIView):
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of reviews for a product', ReviewSerializer(many=True)),
        },
        tags=['Reviews'],
        operation_summary = 'List of reviews for a specific product',
    )
    def get(self, request, product_id):
        reviews = self.get_reviews(product_id)
        serializer = self.serializer_class(instance=reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_reviews(self, product_id):
        """
        Helper function to retrieve reviews for a product.
        """
        return Review.objects.filter(product_id=product_id)
    

class ReviewDetailView(APIView):
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Details of a review', ReviewSerializer),
            404: 'Review not found',
        },
        tags=['Reviews'],
        operation_summary = 'Details for a specific review',
    )
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = self.serializer_class(instance=review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ReviewUpdateView(APIView):
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating'),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Review comment'),
            },
        ),
        responses={
            200: openapi.Response('Review successfully updated', ReviewSerializer),
            400: 'Invalid input data',
            404: 'Review not found',
        },
        tags=['Reviews'],
        operation_summary = 'Update a specific review',
    )
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = self.serializer_class(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ReviewDeleteView(APIView):
    @swagger_auto_schema(
        responses={
            204: 'Review successfully deleted',
            404: 'Review not found',
        },
        tags=['Reviews'],
        operation_summary = 'Delete a specific review',
    )
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




'''
CATEGORY APIS
'''


class CategoryCreateView(APIView):
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the category'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the category'),
            },
            required=['name']
        ),
        responses={
            201: openapi.Response('Category successfully created', CategorySerializer),
            400: 'Invalid input data',
        },
        tags=['Categories'],
        operation_summary = 'Create a category',
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Category successfully created',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of categories', CategorySerializer(many=True)),
        },
        tags=['Categories'],
        operation_summary = 'Get a list of all categories',
    )
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = self.serializer_class(instance=categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Details of a category', CategorySerializer),
            404: 'Category not found',
        },
        tags=['Categories'],
        operation_summary = 'Get details of a specific category',
    )
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(instance=category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CategoryUpdateView(APIView,IsStaffMixin, IsAdminMixin):
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Updated name of the category'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Updated description'),
            },
        ),
        responses={
            200: openapi.Response('Category successfully updated', CategorySerializer),
            400: 'Invalid input data',
            404: 'Category not found',
        },
        tags=['Categories'],
        operation_summary = 'Update a specific category',
    )
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        data = request.data
        serializer = self.serializer_class(instance=category, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Category successfully updated',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView,IsStaffMixin,IsAdminMixin):
    @swagger_auto_schema(
        responses={
            204: 'Category successfully deleted',
            404: 'Category not found',
        },
        tags=['Categories'],
        operation_summary = 'Delete a specific category',
    )
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    


'''SELLER APIS'''
class ProductCreateView(generics.ListCreateAPIView, IsAdminMixin):
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






class SellerOrdersAPIView(APIView, IsSellerMixin):
    @swagger_auto_schema(
        tags=["Seller"],
        operation_summary="Get Seller Orders",
        operation_description="Get all orders associated with the authenticated seller.",
        responses={200: CartItemSerializer(many=True)}
    )
    def get(self, request):
        # Assuming the seller is authenticated and available in the request
        seller = request.user.seller
        seller_orders = CartItem.objects.filter(product__seller=seller).distinct()
        serializer = CartItemSerializer(seller_orders, many=True)
        return Response(serializer.data)


'''CART APIS'''

class CartView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Cart details', CartSerializer),
            404: 'Cart not found',
        },
        tags=['Cart'],
        operation_summary = 'Get the cart and all the items in it',
    )

    

    def get(self, request):
        user = request.user
        order, created= Cart.objects.get_or_create(user=user)
        serializer = self.serializer_class(order)

        return Response(data= serializer.data, status=status.HTTP_200_OK )
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'key': openapi.Schema(type=openapi.TYPE_STRING),
                'value': openapi.Schema(type=openapi.TYPE_STRING),
        
            }
        ),
        responses={
            202: openapi.Response('Cart updated successfully', CartSerializer),
            400: 'Invalid input data',
        },
        tags=['Cart'],
        operation_summary = 'Update the cart address',
    )
    
    def put(self,request):
        user = request.user
        order = get_object_or_404(Cart, user=user)
        serializer= self.serializer_class(order, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status= status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)







class AddToCartView(APIView):
   serializer_class = CartItemSerializer
   permission_classes = [IsAuthenticated]

   @swagger_auto_schema(
        tags=['Cart'],
        operation_summary="Retrieve cart items for the current user",
        operation_description="This endpoint retrieves the cart items for the current user.",
        responses={status.HTTP_200_OK: CartItemSerializer(many=True)}
    )

   def get(self,request, *args, **kwargs):
       user = request.user
       order, created = Cart.objects.get_or_create(user=user)
       cart_items = order.cart_items.all()
       serializer = self.serializer_class(cart_items, many=True)

       return Response(data=serializer.data, status= status.HTTP_200_OK)
   

   @swagger_auto_schema(
        tags=['Cart'],
        operation_summary="Add a product to the cart",
        operation_description="This endpoint adds a product to the user's cart.",
        request_body=CartItemSerializer,
        responses={status.HTTP_201_CREATED: CartItemSerializer, status.HTTP_400_BAD_REQUEST: "Bad Request"}
    )
   

   def post(self,request):
       user = request.user
       order, created = Cart.objects.get_or_create(user=user)
       serializer = self.serializer_class(data=request.data,)
       if serializer.is_valid():
           serializer.save()
           return Response(data=serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   
class UpdateCartItem(APIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific cart item",
        operation_description="This endpoint returns details of a cart item identified by its primary key.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        
        tags=['Cart'],
    )
    def get(self, request, pk):
        user = request.user
        order, created = Cart.objects.get_or_create(user=user)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a specific cart item",
        operation_description="This endpoint updates the details of a specific cart item identified by its primary key.",
        request_body=CartItemSerializer,
        responses={status.HTTP_202_ACCEPTED: CartItemSerializer, status.HTTP_400_BAD_REQUEST: "Bad Request"},
        tags=['Cart'],
    )
    def put(self, request, pk):
        user = request.user
        order, created = Cart.objects.get_or_create(user=user)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save(partial=True)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItem(APIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific cart item",
        operation_description="This endpoint returns details of a cart item identified by its primary key.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        tags=['Cart'],
    )
    def get(self, request, pk):
        user = request.user
        order, created = Cart.objects.get_or_create(user=user)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a specific cart item",
        operation_description="This endpoint deletes a specific cart item identified by its primary key.",
        responses={status.HTTP_204_NO_CONTENT: "Cart item successfully deleted"},
        tags=['Cart'],
    )
    def delete(self, request, pk):
        user = request.user
        order, created = Cart.objects.get_or_create(user=user)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        cart_item.delete()
        response = {'message': 'Cart item successfully deleted'}
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)
    

'''ADDRESS API'''

class BillingAddressListCreateAPIView(generics.ListCreateAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all billing addresses or create a new one.",
        responses={200: BillingAddressSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new billing address.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'city': openapi.Schema(type=openapi.TYPE_STRING),
                'state': openapi.Schema(type=openapi.TYPE_STRING),
                'zipcode': openapi.Schema(type=openapi.TYPE_STRING),
                'is_billing_address': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        ),
        responses={201: BillingAddressSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BillingAddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a billing address by ID.",
        responses={200: BillingAddressSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a billing address by ID.",
        request_body=BillingAddressSerializer,
        responses={200: BillingAddressSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a billing address by ID.",
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)






#ADMIN VIEWS




    
class OrdersView(APIView,IsStaffMixin, IsAdminMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve details of all orders by customers",
        operation_description="This endpoint returns details of orders.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        tags=['Cart'],
    )


    def get(self, request):
        orders = Cart.objects.all()
        serializer = self.serializer_class(orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class OrderDetailView(APIView,IsStaffMixin, IsAdminMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve details of specific orders by customers",
        operation_description="This endpoint returns details of specific orders for the admin.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        tags=['Cart'],
    )

    
    def get(self, request, pk):
        order = get_object_or_404(Cart, pk=pk)
        serializer = self.serializer_class(order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class AdminOrderUpdateDeleteView(APIView, IsAdminMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve details of specific orders by customers",
        operation_description="This endpoint returns details of specific orders for the admin.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        tags=['Cart'],
    )

    
    def put(self, request, pk):
        data= request.data
        order = get_object_or_404(Cart, pk=pk)
        serializer = self.serializer_class(data,order)
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AdminUpdateDeleteCartItem(APIView, IsAdminMixin):
    serializer_class = CartItemSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific cart item",
        operation_description="This endpoint returns details of a cart item identified by its primary key.",
        responses={status.HTTP_200_OK: CartItemSerializer},
        tags=['Cart'],
    )
    def get(self, request, cart_pk, pk):
        order = get_object_or_404(Cart, pk=cart_pk)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a specific cart item",
        operation_description="This endpoint updates the details of a specific cart item identified by its primary key.",
        request_body=CartItemSerializer,
        responses={status.HTTP_200_OK: CartItemSerializer, status.HTTP_204_NO_CONTENT: "Cart item successfully deleted", status.HTTP_400_BAD_REQUEST: "Bad Request"},
        tags=['Cart'],
    )
    def put(self, request, cart_pk, pk):
        order = get_object_or_404(Cart, pk=cart_pk)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        serializer = self.serializer_class(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save(partial=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a specific cart item",
        operation_description="This endpoint deletes a specific cart item identified by its primary key.",
        responses={status.HTTP_204_NO_CONTENT: "Cart item successfully deleted"},
        tags=['Cart'],
    )
    def delete(self, request, cart_pk, pk):
        order = get_object_or_404(Cart, pk=cart_pk)
        cart_item = get_object_or_404(CartItem, order=order, pk=pk)
        cart_item.delete()
        response = {'message': 'Cart item successfully deleted'}
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)



class PromotionListCreateAPIView(generics.ListCreateAPIView, IsAdminMixin):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="List Promotions",
        operation_description="Get a list of all promotions.",
        responses={200: PromotionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Create Promotion",
        operation_description="Create a new promotion.",
        request_body=PromotionSerializer,
        responses={201: PromotionSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PromotionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, IsAdminMixin):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Retrieve Promotion",
        operation_description="Retrieve details of a specific promotion.",
        responses={200: PromotionSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Update Promotion",
        operation_description="Update details of a specific promotion.",
        request_body=PromotionSerializer,
        responses={200: PromotionSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["promotion"],
        operation_summary="Delete Promotion",
        operation_description="Delete a specific promotion."
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
    
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, IsAdminMixin):
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
        partial = kwargs.pop('partial', False)
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
        kwargs['partial'] = True
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
            200: openapi.Response('List of Sellers', SellerSerializer(many=True)),
            201: openapi.Response('Created Seller', SellerSerializer),
        },
        tags=['Sellers'],
        operation_summary = 'Get a list of all sellers',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['company_name', 'address', 'phone_number'],
        ),
        responses={
            201: openapi.Response('Created Seller', SellerSerializer),
        },
        tags=['Sellers'],
        operation_summary = 'Create a seller',
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class SellerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView, IsAdminMixin, IsStaffMixin):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Details of a seller', SellerSerializer),
            404: 'Seller not found',
        },
        tags=['Sellers'],
        operation_summary = 'Update details of a specific  seller',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['company_name'],  # Specify required properties here
        ),
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Details of a seller', SellerSerializer),
            204: 'No Content',
            404: 'Seller not found',
        },
        tags=['Sellers'],
        operation_summary = 'Delete a seller',
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class UserProfileView(APIView, IsStaffMixin):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: UserSerializer()},
        operation_summary="Get user profile",
        operation_description="Get the profile of the authenticated user."
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
        operation_description="List all billing addresses for a user by user ID.",
        responses={200: BillingAddressSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            queryset = self.get_queryset().filter(customer__id=user_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)


class AdminBillingAddressDetailAPIView(generics.RetrieveAPIView):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a billing address by its ID.",
        responses={200: BillingAddressSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


