from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
