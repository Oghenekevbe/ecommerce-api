from django.urls import path
from .views import (
    SellerListCreateView,
    SellerRetrieveUpdateDestroyView,
    OrderView,
    AdminUpdateDeleteCartItem,
    PromotionListCreateAPIView,
    PromotionRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    UserProfileView,
    AdminUserBillingAddressesAPIView,
    AdmincartHistory,
    CategoryListCreateView,
    CategoryRetrieveUpdateDeleteView
)


urlpatterns = [
    # ADMIN ENDPOINTS
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-retrieve-update-delete'),
    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/<str:pk>/", OrderView.as_view(), name="order-detail-update-delete"),
    path("order/<str:cart_pk>/item/<str:pk>/", AdminUpdateDeleteCartItem.as_view(), name="admin_update_delete_cart_item"),
    path("promotions/", PromotionListCreateAPIView.as_view(), name="promotion-list-create"),
    path("promotions/<int:pk>/", PromotionRetrieveUpdateDestroyAPIView.as_view(), name="promotion-retrieve-update-destroy"),
    path("products/", ProductListCreateAPIView.as_view(), name="admin-product-list-create"),
    path("products/<int:pk>/", ProductRetrieveUpdateDestroyAPIView.as_view(), name="admin-product-retrieve-update-destroy"),
    path("sellers/", SellerListCreateView.as_view(), name="seller-list-create"),
    path("sellers/<int:pk>/", SellerRetrieveUpdateDestroyView.as_view(), name="seller-retrieve-update-destroy"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("billing-addresses/", AdminUserBillingAddressesAPIView.as_view(), name="admin-user-billing-addresses"),
    path("order_history/<str:pk>/", AdmincartHistory.as_view(), name="admin_order_history"),
]