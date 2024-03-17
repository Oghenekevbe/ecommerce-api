import requests
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import LoginSerializer, UserSerializer
from .tokens import get_tokens_for_user
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.base import View
from rest_framework.permissions import AllowAny

# Create your views here.

User = get_user_model()


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


class GoogleAuthRedirect(View):
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri=http://localhost:8000/auth/google/callback/"
        return HttpResponseRedirect(redirect_url)


class GoogleRedirectURIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Extract the authorization code from the request URL
        code = request.GET.get("code")

        if code:
            # Prepare the request parameters to exchange the authorization code for an access token
            token_endpoint = "https://oauth2.googleapis.com/token"
            token_params = {
                "code": code,
                "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                "redirect_uri": request.build_absolute_uri(
                    reverse("google-callback")
                ),  # Must match the callback URL configured in your Google API credentials
                "grant_type": "authorization_code",
            }

            # Make a POST request to exchange the authorization code for an access token
            response = requests.post(token_endpoint, data=token_params)

            if response.status_code == 200:
                access_token = response.json().get("access_token")

                if access_token:
                    # Make a request to fetch the user's profile information
                    profile_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo"
                    headers = {"Authorization": f"Bearer {access_token}"}
                    profile_response = requests.get(profile_endpoint, headers=headers)

                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        # Proceed with user creation or login

                        print("creating a user")
                        user = User.objects.create_user(
                            first_name=profile_data["given_name"],
                            email=profile_data["email"],
                        )

                        print("testing ooooooooo", user.first_name, user.email)
                        if "family_name" in profile_data:
                            print(
                                "Before save:",
                                user.first_name,
                                user.last_name,
                                user.email,
                            )
                            user.last_name = profile_data.get("family_name", "")
                            user.save()
                            print(
                                "After save:",
                                user.first_name,
                                user.last_name,
                                user.email,
                            )

                            print("USER:   ", user)
                        refresh = get_tokens_for_user(user)
                        data["access"] = refresh["access"]
                        data["refresh"] = [refresh]
                        return Response(data, status=status.HTTP_201_CREATED)

        return Response({}, status.HTTP_400_BAD_REQUEST)
