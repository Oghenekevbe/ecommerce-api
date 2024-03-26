import jwt
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise AuthenticationFailed("User account is not active.")
                data["user"] = user
                return data
            else:
                raise AuthenticationFailed("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")


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
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        user.is_active = False
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    # validate method ensures that the new password matches the confirmed password.
    # validate_new_password method utilizes Django's built-in password validation to ensure that the new password meets the required complexity criteria.

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("The new passwords do not match")
        return data

    def validate_new_password(self, value):
        validate_password(value)
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the database.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address does not exist.")
        return value

    def create(self, validated_data):
        """
        This method should be implemented, but since we don't create any new
        model instance, we return None.
        """
        return None


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        token = data.get("token")
        new_password = data.get("new_password")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get("email")
            user = User.objects.get(email=email)
            # Additional validation if needed
            if not user.is_active:
                raise ValidationError("User is not active.")
        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired.")
        except (jwt.DecodeError, jwt.InvalidTokenError, User.DoesNotExist):
            raise ValidationError("Invalid token.")

        # Store the user object and new password for use in the save() method
        self.user = user
        self.new_password = new_password
        return data

    def save(self, **kwargs):
        # Change the user's password
        self.user.set_password(self.new_password)
        self.user.save()
