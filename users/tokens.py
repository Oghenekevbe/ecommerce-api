from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from datetime import datetime, timedelta


def get_tokens_for_email(email):
    # Define payload with email address and expiration time
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=1),  # Token expires in 1 day
    }
    # Generate JWT access token
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    # Generate JWT refresh token
    refresh_payload = {
        "email": email,
        "exp": datetime.utcnow()
        + timedelta(days=30),  # Refresh token expires in 30 days
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    tokens = {"access": access_token, "refresh": refresh_token}

    return tokens


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["email"] = user.email  # Add the email to the token payload
        return token


def get_tokens_for_user(user):
    refresh = CustomRefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
