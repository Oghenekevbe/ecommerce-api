from django.db import models
from store.models import Cart

# Create your models here.

PAYMENT_CHOICES = (
    ("flutterwave", "Flutterwave"),
    ("paystack", "Paystack"),
    ("remita", "Remita"),
)


class PaymentModel(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    mode_of_payment = models.CharField(
        max_length=30, null=True, choices=PAYMENT_CHOICES
    )

    def __str__(self):
        return f"{self.order.user} - {self.order.order_number} - {self.mode_of_payment}"
