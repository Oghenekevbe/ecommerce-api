from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import CustomLoginView, GoogleAuthRedirect, GoogleRedirectURIView

urlpatterns = [
    path("api/token/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/login/", CustomLoginView.as_view(), name="login_view"),
    re_path(r"^auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("api/google-signup/", GoogleAuthRedirect.as_view()),
    path(
        "auth/google/callback/",
        GoogleRedirectURIView.as_view(),
        name="google-callback",
    ),
]
