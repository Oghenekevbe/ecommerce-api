from django.db import models
from store.models import Cart



class PaymentModel(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order.user} - {self.order.order_number}"
