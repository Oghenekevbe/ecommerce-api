# import jwt
# from django.contrib.auth import authenticate
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.sites.shortcuts import get_current_site
# from django.http import HttpResponse, JsonResponse
# from .serializers import (
#     LoginSerializer,
#     CreateUserSerializer,
#     ChangePasswordSerializer,
#     PasswordResetSerializer,
#     PasswordResetRequestSerializer,
# )
# from .tokens import get_tokens_for_user, get_tokens_for_email
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework import permissions
# from rest_framework_simplejwt.tokens import RefreshToken


# from django.core.mail import BadHeaderError
# from django.core.mail import EmailMessage
# from django.http import HttpResponse


# # Create your views here.

# User = get_user_model()


# class CustomLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = LoginSerializer

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["email", "password"],
#             properties={
#                 "email": openapi.Schema(type=openapi.TYPE_STRING),
#                 "password": openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         responses={
#             200: "Login Successful",
#             401: "Invalid email or password",
#         },
#     )
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             password = serializer.validated_data["password"]

#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 if user.is_active:
#                     tokens = get_tokens_for_user(user)
#                     return Response(
#                         {
#                             "message": "Login successful",
#                             "Tokens": tokens,
#                         },
#                         status=status.HTTP_200_OK,
#                     )
#                 else:
#                     raise AuthenticationFailed("User account is not active.")
#             else:
#                 raise AuthenticationFailed("Invalid email or password.")
#         else:
#             return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# class UserEmailRegistration(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = CreateUserSerializer

#     def post(self, request, *args, **kwargs):

#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             print("serializer is valid")

#             user = serializer.save()
#             tokens = get_tokens_for_user(user)
#             refresh_token = tokens["refresh"]
#             to_email = user.email
#         self.send_email(request, refresh_token, to_email)
#         response = {
#             "message": "Kindly check your E-mail for a confirmation message in order to complete registration"
#         }
#         return Response(data=response, status=status.HTTP_201_CREATED)

#     def send_email(self, request, refresh_token, to_email):
#         subject = "Confirm your Email Address"
#         domain = get_current_site(request).domain
#         url = f"{domain}/api/confirm_email/?to_email={to_email}&refresh_token={refresh_token}"
#         message = f"Hello, \n Kindly click the link below to confirm your address:\n {url} \n Token : {refresh_token}"
#         from_email = settings.EMAIL_HOST_USER  # Use the configured sender email

#         # Validate recipient email address
#         if not to_email:
#             return HttpResponse("Recipient email is required.")

#         try:
#             # Create an EmailMessage object
#             confirm_message = EmailMessage(
#                 subject,
#                 message,
#                 from_email,
#                 [to_email],
#                 headers={"Message-ID": "foo"},
#             )

#             # Send the email
#             confirm_message.send()
#         except BadHeaderError:
#             return HttpResponse("Invalid header found.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred while sending the email: {str(e)}")


# @api_view(["GET", "POST"])
# @permission_classes([AllowAny])
# def ActivateEmail(request, pk=None):

#     if request.method == "GET":
#         refresh_token = request.GET.get("refresh_token")

#         print("refresh token: ", refresh_token)
#         to_email = request.GET.get("to_email")

#         print("to_email: ", to_email)
#         try:
#             # Decode the JWT token using the secret key
#             payload = jwt.decode(
#                 refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
#             )

#             # Extract user information from the decoded payload
#             user_id = payload["user_id"]

#             print("user id:  ", user_id)
#             email = payload["email"]

#             print("email : ", email)

#             # Check if the email in the token matches the provided 'to_email'
#             if email == to_email:

#                 print("emails are the same")

#                 # Retrieve the user object from the database using the user_id
#                 user = User.objects.get(email=email)

#                 print("this is the user ooooo", user)

#                 # Perform email activation logic here

#                 user.is_active = True
#                 user.save()

#                 # Generate a new access token using the provided refresh token
#                 refresh = RefreshToken(refresh_token)
#                 access_token = str(refresh.access_token)

#                 response = {
#                     "message": "Email confirmed successfully. Profile is now active",
#                     "access_token": access_token,
#                 }

#                 # Respond with the new access token
#                 return JsonResponse(data=response, status=status.HTTP_200_OK)

#                 # Respond with a success message or activate the email
#                 return HttpResponse("Email activated successfully")
#             else:
#                 # If the provided 'to_email' does not match the email in the token,
#                 # respond with an error message
#                 return HttpResponse(
#                     "Invalid email for the user associated with the token"
#                 )

#         except jwt.ExpiredSignatureError:
#             # Handle the case where the token has expired
#             return HttpResponse("Token has expired")

#         except jwt.InvalidTokenError:
#             # Handle the case where the token is invalid or tampered with
#             return HttpResponse("Invalid token")

#         except User.DoesNotExist:
#             # Handle the case where the user does not exist
#             return HttpResponse("User not found")


# class ChangePasswordView(APIView):
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             old_password = serializer.validated_data["old_password"]
#             new_password = serializer.validated_data["new_password"]
#             confirm_password = serializer.validated_data["confirm_password"]

#             if not user.check_password(old_password):
#                 return Response(
#                     {"error": "Incorrect old password."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if new_password == old_password:
#                 return Response(
#                     {"error": "New password must be different from old password."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             user.set_password(new_password)
#             user.save()
#             tokens = get_tokens_for_user(user)

#             return Response(
#                 {"message": "Password changed successfully.", "Tokens": tokens},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetRequestView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = PasswordResetRequestSerializer

#     def post(self, request, *args, **kwargs):

#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             print("serializer is valid")

#             email = serializer.validated_data.get("email")
#             if email:
#                 # Perform further actions with the validated email
#                 # For example, sending the reset email
#                 tokens = get_tokens_for_email(email)
#                 refresh_token = tokens
#                 self.send_email(request, refresh_token, email)
#                 response = {
#                     "message": "Kindly check your E-mail to confirm your request"
#                 }
#                 return Response(data=response, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(
#                     {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
#                 )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def send_email(self, request, refresh_token, to_email):
#         subject = "Password Reset"
#         domain = get_current_site(request).domain
#         message = f"Hello, Here is your token:\n{refresh_token}\n If you did not request this service, do nothing"
#         from_email = settings.EMAIL_HOST_USER  # Use the configured sender email

#         # Validate recipient email address
#         if not to_email:
#             return HttpResponse("Recipient email is required.")

#         try:
#             # Create an EmailMessage object
#             confirm_message = EmailMessage(
#                 subject,
#                 message,
#                 from_email,
#                 [to_email],
#                 headers={"Message-ID": "foo"},
#             )

#             # Send the email
#             confirm_message.send()
#         except BadHeaderError:
#             return HttpResponse("Invalid header found.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred while sending the email: {str(e)}")


# class PasswordResetView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = PasswordResetSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Password reset successful."}, status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.http import HttpResponseRedirect
from django.conf import settings 
def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )

def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


# from allauth.account.models import EmailConfirmationHMAC, EmailAddress
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# class ResendVerifyEmail(APIView):

#     def post(self, request):
#         data = request.data
#         email = data['email']
#         try:
#             email_address = EmailAddress.objects.get(email=email)
#             print('email = ', email)
#             emac = EmailConfirmationHMAC(email_address=email_address)
#             print("emac = ", emac)
#             emac.send(request, signup=True)

#             return Response({'msg': 'The verification email has been sent'}, status=status.HTTP_201_CREATED)
#         except EmailAddress.DoesNotExist:
#             return Response({'msg': 'No such user, register first'})

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ResendVerifyEmail(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        
        if not email:
            return Response({'msg': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            email_address = EmailAddress.objects.get(email=email)
        except EmailAddress.DoesNotExist:
            return Response({'msg': 'No such user, register first'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the email is already verified
        if email_address.verified:
            return Response({'msg': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)

        # Send the verification email
        send_email_confirmation(request, email_address.user)
        
        return Response({'msg': 'The verification email has been sent'}, status=status.HTTP_200_OK)
