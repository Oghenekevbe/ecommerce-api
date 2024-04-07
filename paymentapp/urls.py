from django.urls import path
from .views import (
    orderCompletedView,
)

urlpatterns = [
    # PAYMENT ENDPOINTS
    path(
        "api/payment_completed/", orderCompletedView.as_view(), name="payment_completed"
    ),
]
