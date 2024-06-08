from django.contrib import admin
from .models import (
    Product,
    Category,
    BillingAddress,
    Cart,
    CartItem,
    Review,
    Promotion,
    Return,
)

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin View for"""

    list_display = (
        "name",
        "price",
        "discounted_price",
        "stock_status",
        "created_by",
        "updated_by",
        "created_at",
    )

    ordering = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin View for"""

    list_display = ("name", "description")

    ordering = [
        "name",
    ]




@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "address",
        "city",
        "state",
        "zipcode",
        "date_added",
        "is_billing_address",
    )
    ordering = ("customer",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "address",
        "date_ordered",
        "status",
        "is_active",
        "order_number",
        "cart_total",
        "cart_item_count",
    )
    ordering = ("-date_ordered",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "order",
        "quantity",
        "date_ordered",
        "get_total",
        "status",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "comment", "created_at")
    list_filter = ("product", "user", "created_at")
    search_fields = ("product__name", "user__username", "comment")


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_display = (
        "promo_name",
        "discount_percentage",
        "start_date",
        "end_date",
        "description",
    )


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ("order", "returned_item", "return_reason", "return_date")
