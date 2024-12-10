from rest_framework import serializers
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
    seller = SellerSerializer(source="product.seller", read_only=True)
    discounted_price = serializers.ReadOnlyField(source="product.discounted_price")
    get_total = serializers.ReadOnlyField()
    status = OrderStatusSerializer()

    class Meta:
        model = CartItem
        fields = [
            "id", "product", "name", "order", "quantity", "price", "seller",
            "discounted_price", "get_total", "date_ordered", "status"
        ]

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