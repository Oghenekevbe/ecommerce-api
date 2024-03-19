from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import CustomLoginView, UserEmailRegistration

urlpatterns = [
    path("api/token/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/login/", CustomLoginView.as_view(), name="login_view"),
    path(
        "api/signup/email/",
        UserEmailRegistration.as_view(),
        name="email_registration_view",
    ),
    path(
        "api/confirm_email/",
        views.ActivateEmail,
        name="confirm_email",
    ),
]
