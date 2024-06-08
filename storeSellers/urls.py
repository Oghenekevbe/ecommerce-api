from django.urls import path
from .views import (
    ProductCreateView,
    SellerOrdersAPIView,
)


urlpatterns = [
    # SELLER ENDPOINTS
    path("api/products/create/", ProductCreateView.as_view(), name="product-create"),
    path("api/seller/orders/", SellerOrdersAPIView.as_view(), name="seller-orders"),
]
