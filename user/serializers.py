from .models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                attrs["user"] = user
                return attrs
            raise serializers.ValidationError("Invalid email or password.")
        raise serializers.ValidationError('Must include "email" and "password".')
