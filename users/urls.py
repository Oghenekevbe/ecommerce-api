
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from .views import ResendVerifyEmail
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import path
from users.views import email_confirm_redirect, password_reset_confirm_redirect

urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_register"),  # Handles user registration.
    path('account-email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),  # Shows a confirmation page or message after the user has successfully requested email verification.
    path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),  # Handles email verification when the user clicks the verification link in their email.
    path("register/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),  # Provides an endpoint for the email verification process. It should match the URL used in the verification email sent to users.
    path("register/resend-email/", ResendVerifyEmail.as_view(), name="rest_resend_email"),  # Allows users to request a new verification email if they didn't receive the initial one or if it expired.

    path("login/", LoginView.as_view(), name="rest_login"),  # Handles user login.
    path("logout/", LogoutView.as_view(), name="rest_logout"),  # Handles user logout.
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),  # Provides user details. This endpoint typically returns information about the currently authenticated user.

    path("password/change/", PasswordChangeView.as_view(), name="password_change"),  # Allows users to change their password.
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),  # Initiates the password reset process.
    path("password/reset/confirm/<str:uidb64>/<str:token>/", password_reset_confirm_redirect, name="password_reset_confirm"),  # Handles the confirmation of a password reset. Users visit this URL (with the appropriate `uidb64` and `token`) to reset their password.
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),  # Provides an endpoint to confirm the password reset process after the user clicks on the reset link from their email.
]
