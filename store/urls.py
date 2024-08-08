from django.urls import path
from .views import (
    ProductView,
    ProductSearch,
    ReviewView,
    CartItemView,
    CartView,
    BillingAddressListCreateAPIView,
    BillingAddressRetrieveUpdateDestroyAPIView,
    CartHistory,
)


urlpatterns = [
    # USER ENDPOINT
    path(
        "api/billing-addresses/",
        BillingAddressListCreateAPIView.as_view(),
        name="billing-address-list-create",
    ),
    path(
        "api/billing-addresses/<int:pk>/",
        BillingAddressRetrieveUpdateDestroyAPIView.as_view(),
        name="billing-address-retrieve-update-destroy",
    ),
    # PRODUCT ENDPOINTS
    path("api/products/", ProductView.as_view(), name="products"),
    path("api/products/<int:pk>/", ProductView.as_view(), name="product-detail"),
    path("api/search/", ProductSearch.as_view(), name="search"),


    # PRODUCT REVIEW ENDPOINTS
    path('reviews/', ReviewView.as_view(), name='review-list'),
    path('reviews/<int:review_id>/', ReviewView.as_view(), name='review-detail'),
    path('products/<int:product_id>/reviews/', ReviewView.as_view(), name='product-reviews'),

    # CART ENDPOINTS
    path("api/cart/", CartView.as_view(), name="cart-view"),
     path('cart-items/', CartItemView.as_view(), name='cart-item-list'),
    path('cart-items/<int:pk>/', CartItemView.as_view(), name='cart-item-detail'),
    path("api/order_history/", CartHistory.as_view(), name="oder_history"),
]
