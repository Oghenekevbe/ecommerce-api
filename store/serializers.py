from rest_framework import serializers
from .models import Category, Product, Review, Seller,Cart,CartItem,BillingAddress
from user.models import User

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'rating', 'comment', 'created_at')

class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField()
    reviews = ReviewSerializer(many=True, read_only=True)  # Include reviews in the serialized output
    stock_status = serializers.ReadOnlyField()
    seller = serializers.StringRelatedField(many=True, source='product.seller.all', read_only=True)
    promo = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'user', 'name','category', 'description',  'price', 'discount_percentage','discounted_price','promo','image',
            'is_available',  'created_at', 'updated_at',
            'sku',
             'stock_status', 'manufacturer', 'stock_quantity', 'restock_threshold', 'seller', 'reviews'
        ]
 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class SellerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = Seller
        fields = ['id', 'user', 'company_name', 'address', 'phone_number']

class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ['id', 'customer', 'address', 'city', 'state', 'zipcode', 'date_added', 'is_billing_address']

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product.id'
    )
    quantity = serializers.IntegerField()
    price = serializers.ReadOnlyField(source='product.price')
    discounted_price = serializers.ReadOnlyField(source='product.discounted_price')
    get_total = serializers.ReadOnlyField()



    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'order',  'date_ordered','quantity', 'price', 'discounted_price', 'get_total']

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    





class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'address', 'date_ordered', 'status', 'order_number', 'cart_items', 'cart_total']
        read_only_fields = ['user',  'date_ordered',  'order_number', 'cart_items', 'cart_total']


