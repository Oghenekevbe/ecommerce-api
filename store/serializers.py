from rest_framework import serializers
from .models import Category, Product, Review, Seller,Cart,CartItem,BillingAddress
from user.models import User

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'rating', 'comment', 'created_at')

class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)  # Include reviews in the serialized output
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
 
    def get_discounted_price(self, obj):
        discount_factor = 1 - (obj.discount_percentage/100)
        discounted_price = obj.price * discount_factor
        return round(discounted_price, 2)
    
    def get_stock_status(self, obj):
        return obj.stock_status
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Seller
        fields = ['id', 'user', 'company_name', 'address', 'phone_number']

class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['id', 'customer', 'address', 'city', 'state', 'zipcode', 'date_added', 'is_no_billing_address']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'order', 'quantity', 'date_ordered', 'product_name']

    def get_product_name(self, obj):
        return obj.product.name

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    billing_address = BillingAddressSerializer()
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'billing_address', 'date_ordered', 'complete', 'transaction_id', 'cart_items']

class CartTotalSerializer(serializers.Serializer):
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)

