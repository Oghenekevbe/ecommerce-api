from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductSearch,
    ReviewCreateView,
    ReviewListView,
    ReviewDetailView,
    ReviewUpdateView,
    ReviewDeleteView,
    CartView,
    AddToCartView,
    UpdateCartItem,
    DeleteCartItem,
    BillingAddressListCreateAPIView,
    BillingAddressRetrieveUpdateDestroyAPIView,
    cartHistory,
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
    path("api/products/", ProductListView.as_view(), name="product-list"),
    path("api/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("api/search/", ProductSearch.as_view(), name="search"),
    # PRODUCT REVIEW ENDPOINTS
    path("api/reviews/", ReviewCreateView.as_view(), name="review-create"),
    path("api/reviews/<int:product_id>/", ReviewListView.as_view(), name="review-list"),
    path(
        "api/reviews/detail/<int:review_id>/",
        ReviewDetailView.as_view(),
        name="review-detail",
    ),
    path(
        "api/reviews/update/<int:review_id>/",
        ReviewUpdateView.as_view(),
        name="review-update",
    ),
    path(
        "api/reviews/delete/<int:review_id>/",
        ReviewDeleteView.as_view(),
        name="review-delete",
    ),

    # CART ENDPOINTS
    path("api/cart/", CartView.as_view(), name="cart-view"),
    path("api/add_to_cart/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "api/update_cart_item/<str:pk>/",
        UpdateCartItem.as_view(),
        name="update_cart_item",
    ),
    path(
        "api/delete_cart_item/<str:pk>/",
        DeleteCartItem.as_view(),
        name="delete_cart_item",
    ),
    path("api/order_history/", cartHistory.as_view(), name="oder_history"),
]
