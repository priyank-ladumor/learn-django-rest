from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, VerifyOTPSerializer, ResetPasswordSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from authapi.models import PasswordResetOTP

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # permission_classes = (AllowAny,)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return  Response({'access': str(refresh.access_token),'refresh': str(refresh), 'user': user_serializer.data})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=404)

        # Generate OTP
        otp = get_random_string(length=6, allowed_chars='0123456789')
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # Send Email
        send_mail(
            subject='Your OTP for password reset',
            message=f'Your OTP is: {otp}',
            from_email='noreply@example.com',
            recipient_list=[email],
        )

        return Response({'message': 'OTP sent to email'}, status=200)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid email.'}, status=404)

        try:
            otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            return Response({'message': 'Invalid OTP.'}, status=400)

        # Check if OTP is expired (valid for 10 minutes)
        if timezone.now() > otp_entry.created_at + timedelta(minutes=10):
            return Response({'message': 'OTP expired.'}, status=400)

        return Response({'message': 'OTP verified.'}, status=200)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Invalid email.'}, status=404)

        try:
            otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            return Response({'message': 'Invalid OTP.'}, status=400)

        # Check expiration
        if timezone.now() > otp_entry.created_at + timedelta(minutes=10):
            return Response({'message': 'OTP expired.'}, status=400)

        # Reset password
        user.set_password(new_password)
        user.save()

        otp_entry.is_used = True
        otp_entry.save()

        return Response({'message': 'Password has been reset successfully.'}, status=200)