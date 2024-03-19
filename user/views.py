import jwt
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from .serializers import LoginSerializer, CreateUserSerializer
from .tokens import get_tokens_for_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken


from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.http import HttpResponse


# Create your views here.

User = get_user_model()


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


class UserEmailRegistration(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print("serializer is valid")

            user = serializer.save()
            print("user oooooooooooo: ", user)
            tokens = get_tokens_for_user(user)
            print(tokens)
            refresh_token = tokens["refresh"]
            to_email = user.email
        self.send_email(request, refresh_token, to_email)
        response = {
            "message": "Kindly check your E-mail for a confirmation message in order to complete registration"
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

    def send_email(self, request, refresh_token, to_email):
        subject = "Confirm your Email Address"
        domain = get_current_site(request).domain
        url = f"{domain}/api/confirm_email/?to_email={to_email}&refresh_token={refresh_token}"
        message = (
            f"Hello, \n Kindly click the link below to confirm your address:\n {url}"
        )
        from_email = settings.EMAIL_HOST_USER  # Use the configured sender email

        # Validate recipient email address
        if not to_email:
            return HttpResponse("Recipient email is required.")

        try:
            # Create an EmailMessage object
            confirm_message = EmailMessage(
                subject,
                message,
                from_email,
                [to_email],
                headers={"Message-ID": "foo"},
            )

            # Send the email
            confirm_message.send()
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        except Exception as e:
            return HttpResponse(f"An error occurred while sending the email: {str(e)}")


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def ActivateEmail(request, pk=None):

    if request.method == "GET":
        refresh_token = request.GET.get("refresh_token")

        print("refresh token: ", refresh_token)
        to_email = request.GET.get("to_email")

        print("to_email: ", to_email)
        try:
            # Decode the JWT token using the secret key
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
            )

            # Extract user information from the decoded payload
            user_id = payload["user_id"]

            print("user id:  ", user_id)
            email = payload["email"]

            print("email : ", email)

            # Check if the email in the token matches the provided 'to_email'
            if email == to_email:

                print("emails are the same")

                # Retrieve the user object from the database using the user_id
                user = User.objects.get(email=email)

                print("this is the user ooooo", user)

                # Perform email activation logic here

                user.is_active = True
                user.save()

                # Generate a new access token using the provided refresh token
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)

                response = {
                    "message": "Email confirmed successfully. Profile is now active",
                    "access_token": access_token,
                }

                # Respond with the new access token
                return JsonResponse(data=response, status=status.HTTP_200_OK)

                # Respond with a success message or activate the email
                return HttpResponse("Email activated successfully")
            else:
                # If the provided 'to_email' does not match the email in the token,
                # respond with an error message
                return HttpResponse(
                    "Invalid email for the user associated with the token"
                )

        except jwt.ExpiredSignatureError:
            # Handle the case where the token has expired
            return HttpResponse("Token has expired")

        except jwt.InvalidTokenError:
            # Handle the case where the token is invalid or tampered with
            return HttpResponse("Invalid token")

        except User.DoesNotExist:
            # Handle the case where the user does not exist
            return HttpResponse("User not found")
