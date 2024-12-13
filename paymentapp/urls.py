from django.urls import path
from . import views
from .views import (
    OrderPayment,
    orderCompletedView,
    paystack_webhook
)

urlpatterns = [
    # PAYMENT ENDPOINTS
    path("api/order_payment/", OrderPayment.as_view(), name="order_payment"),
    path("api/payment_completed/", orderCompletedView.as_view(), name="payment_completed"),
    path('call-back/', views.payment_callback, name='payment_callback'),
    path('webhook/', paystack_webhook, name='paystack_webhook'),
]
