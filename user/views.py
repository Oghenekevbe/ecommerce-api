from .serializers import LoginSerializer, UserSerializer
from .tokens import get_tokens_for_user
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


class CustomSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")


# LOGIN VIEW
class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: "Login Successful",
            401: "Invalid username or password",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            return Response(
                {"message": "Login successful", "Token": tokens["access"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
