from django.urls import path
from .views import (
    SellerListCreateView,
    SellerRetrieveUpdateDestroyView,
    OrdersView,
    OrderDetailView,
    AdminOrderUpdateDeleteView,
    AdminUpdateDeleteCartItem,
    PromotionListCreateAPIView,
    PromotionRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    UserProfileView,
    AdminUserBillingAddressesAPIView,
    AdmincartHistory,
)


urlpatterns = [

    # ADMIN ENDPOINTS
    path("api/admin/orders/", OrdersView.as_view(), name="orders"),
    path(
        "api/admin/order_detail/<str:pk>",
        OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "api/admin/order_update_delete/<str:pk>",
        AdminOrderUpdateDeleteView.as_view(),
        name="order_update_delete",
    ),
    path(
        "api/admin/order/<str:cart_pk>/item/<str:pk>/",
        AdminUpdateDeleteCartItem.as_view(),
        name="admin_update_delete_cart_item",
    ),
    path(
        "api/admin/promotions/",
        PromotionListCreateAPIView.as_view(),
        name="promotion-list-create",
    ),
    path(
        "api/admin/promotions/<int:pk>/",
        PromotionRetrieveUpdateDestroyAPIView.as_view(),
        name="promotion-retrieve-update-destroy",
    ),
    path(
        "api/admin/products/",
        ProductListCreateAPIView.as_view(),
        name="admin-product-list-create",
    ),
    path(
        "api/admin/products/<int:pk>/",
        ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="admin-product-retrieve-update-destroy",
    ),
    path(
        "api/admin/sellers/", SellerListCreateView.as_view(), name="seller-list-create"
    ),
    path(
        "api/admin/sellers/<int:pk>/",
        SellerRetrieveUpdateDestroyView.as_view(),
        name="seller-retrieve-update-destroy",
    ),
    path("api/staff/profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "api/admin/billing-addresses/",
        AdminUserBillingAddressesAPIView.as_view(),
        name="admin-user-billing-addresses",
    ),
    path(
        "api/admin/order_history/<str:pk>/",
        AdmincartHistory.as_view(),
        name="admin_order_history",
    ),
]
