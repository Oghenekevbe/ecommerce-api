from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'is_superuser']