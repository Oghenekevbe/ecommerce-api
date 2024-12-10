from rest_framework import serializers
from store.models import Category
from storeSellers.models import Seller

from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Seller
        fields = ["id", "user", "company_name", "address", "phone_number"]

