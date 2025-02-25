from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, Promotion, Review, Cart, CartItem, BillingAddress, OrderStatus
from storeSellers.models import Seller
from storeAdmin.serializers import SellerSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "product", "user", "rating", "comment", "created_at")



class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField()
    reviews = ReviewSerializer(many=True, read_only=True)
    stock_status = serializers.ReadOnlyField()
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
    promo = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    updated_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "category", "description", "price", "discount_percentage",
            "discounted_price", "promo", "image", "is_available", "created_at",
            "updated_at", "sku", "stock_status", "manufacturer", "stock_quantity",
            "restock_threshold", "seller", "reviews", "created_by", "updated_by"
        ]
        read_only_fields = [
            "created_at", "updated_at", "stock_status", "discounted_price", "seller",
            "promo", "created_by", "updated_by"
        ]
        def validate_image(self, value):
            if value.size > 2 * 1024 * 1024:  # 2MB max size
                raise ValidationError("Image file size exceeds 2MB.")
            if not value.name.endswith(('jpg', 'jpeg', 'png')):
                raise ValidationError("Unsupported file format. Use jpg, jpeg, or png.")
            return value


class ProductListSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "category", "price", "discount_percentage",
            "discounted_price", "promo", "image", "is_available",
            "stock_status", "sku", "seller"
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]

class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = [
            "id", "customer", "address", "city", "state", "zipcode", "date_added",
            "is_billing_address"
        ]

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = [
            "completed", "delivered", "returned", "confirmed", "shipped",
            "processing", "canceled"
        ]

class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="product.name")
    price = serializers.ReadOnlyField(source="product.price")
    discounted_price = serializers.ReadOnlyField(source="product.discounted_price")
    seller = SellerSerializer(source="product.seller", read_only=True)
    get_total = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            "id", "order", "product", "name", "quantity", "price", "discounted_price",
            "seller", "get_total", "date_ordered"
        ]
        read_only_fields = ["id", "name", "order","price", "discounted_price", "seller", "get_total", "date_ordered"]

    def create(self, validated_data):
        """ Ensure the item is added to the user's active cart automatically. """
        user = self.context["request"].user
        order, created = Cart.objects.get_or_create(user=user, is_active=True)

        # Prevent users from adding their own product
        product = validated_data["product"]
        if product.seller.user == user:
            raise serializers.ValidationError("You cannot add your own product to the cart.")

        # Add order reference to validated data
        validated_data["order"] = order

        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    status = OrderStatusSerializer()

    class Meta:
        model = Cart
        fields = [
            "user", "address", "date_ordered", "status", "order_number",
            "cart_items", "cart_item_count", "cart_total"
        ]
        read_only_fields = [
            "user", "date_ordered", "order_number", "cart_items", "cart_total"
        ]