from .models import PaymentModel, Cart
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    mode_of_payment = serializers.CharField()

    class Meta:
        model = PaymentModel
        fields = ["order", "mode_of_payment"]
