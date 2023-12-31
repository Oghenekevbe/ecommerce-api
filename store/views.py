from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Category, Review,BillingAddress,Cart,CartItem,Seller
from .serializers import ProductSerializer, ReviewSerializer, CategorySerializer,SellerSerializer,BillingAddressSerializer,CartItemSerializer,CartSerializer,CartTotalSerializer

class ProductCreateView(APIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the product'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the product'),
                # ... other properties ...
            },
            required=['name']
        ),
        responses={
            201: openapi.Response('Product successfully created', ProductSerializer),
            400: 'Invalid input data',
        },
        tags=['Products'],
    )
    def post(self, request):
        """
        Create a new product.
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Product successfully created',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of products', ProductSerializer(many=True)),
        },
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
    )
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(instance=category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CategoryUpdateView(APIView):
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


class CategoryDeleteView(APIView):
    @swagger_auto_schema(
        responses={
            204: 'Category successfully deleted',
            404: 'Category not found',
        },
        tags=['Categories'],
    )
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    


class SellerListCreateView(generics.ListCreateAPIView):
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
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class SellerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Details of a seller', SellerSerializer),
            404: 'Seller not found',
        },
        tags=['Sellers'],
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
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)







class CartView(APIView):
    '''

        methods=['GET'],
        responses={
            200: openapi.Response('Cart details', CartSerializer),
            404: 'Cart not found',
        }
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, complete=False)
        serializer = self.serializer_class(cart)
        return Response(data= serializer.data, status=status.HTTP_200_OK )
    
    def put(self,request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        serializer= self.serializer_class(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status= status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)







class AddToCartView(APIView):
   pass