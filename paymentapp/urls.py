from django.urls import path
from .views import (
    OrderPayment,
    orderCompletedView,
)

urlpatterns = [
    # PAYMENT ENDPOINTS
    path("api/order_payment/", OrderPayment.as_view(), name="order_payment"),
    path(
        "api/payment_completed/", orderCompletedView.as_view(), name="payment_completed"
    ),
]
