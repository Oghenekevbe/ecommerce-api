from .models import PaymentModel, Cart
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentModel
        fields = "__all__"
