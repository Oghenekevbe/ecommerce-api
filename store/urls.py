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
    path("billing-addresses/", BillingAddressListCreateAPIView.as_view(), name="billing-address-list-create"),
    path("billing-addresses/<int:pk>/", BillingAddressRetrieveUpdateDestroyAPIView.as_view(), name="billing-address-retrieve-update-destroy"),

    # PRODUCT ENDPOINTS
    path("products/", ProductView.as_view(), name="products"),
    path("products/<int:pk>/", ProductView.as_view(), name="product-detail"),
    path("search/", ProductSearch.as_view(), name="search"),
    #e.g http://localhost:8000/api/store/search/?query_type=category&query_value=pets
    #e.g2 http://localhost:8000/api/store/search/?query_type=category&query_value=pets&page=2



    # PRODUCT REVIEW ENDPOINTS
    path('reviews/', ReviewView.as_view(), name='review-list'),
    path('reviews/<int:review_id>/', ReviewView.as_view(), name='review-detail'),
    path('products/<int:product_id>/reviews/', ReviewView.as_view(), name='product-reviews'),

    # CART ENDPOINTS
    path("cart/", CartView.as_view(), name="cart-view"),
     path('cart-items/', CartItemView.as_view(), name='cart-item-list'),
    path('cart-items/<int:pk>/', CartItemView.as_view(), name='cart-item-detail'),
    path("order_history/", CartHistory.as_view(), name="oder_history"),
]
