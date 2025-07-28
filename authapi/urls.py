from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', view=views.RegisterView.as_view(), name='register'),
    path('login/', view=views.LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # token generation
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # token refresh by using refresh token and get new access token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # token verification
    path('forgot-password/', view=views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/', view=views.VerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/', view=views.ResetPasswordView.as_view(), name='reset-password'),
]
