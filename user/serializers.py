from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ["email", "username"]


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


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        print("validation all correct sir")
        return attrs

    def create(self, validated_data):
        password = validated_data["password"]
        # Hash the password
        hashed_password = make_password(password)
        print("we want to create user at the serializer oo")
        user = User.objects.create_user(
            email=validated_data["email"], password=hashed_password
        )
        user.is_active = False
        user.save()

        return user
