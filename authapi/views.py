from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, VerifyOTPAndChangePasswordSerializer, ChangePasswordViewSerializer
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
from django.template.loader import render_to_string
from django.utils.timezone import now

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

        # Check for existing unused OTP
        PasswordResetOTP.objects.update_or_create(
            user=user,
            is_used=False,
            defaults={
                'otp': otp,
                'created_at': now(),
            }
        )
        
        html_content = render_to_string(
            "email/otp_send.html",  # no need to include "templates/"
            context={"otp": otp, "user": user},
        )

        # Send Email
        send_mail(
            subject='Your OTP for password reset',
            message=f'Your OTP is: {otp}',  # fallback plain text
            from_email='priyank.suratinfotech@gmail.com',
            recipient_list=[email],
            html_message=html_content
        )

        return Response({'message': 'OTP sent to email'}, status=200)

class VerifyOTPAndChangePasswordView(APIView):
    def post(self, request):
        serializer = VerifyOTPAndChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        
        if otp:
            try:
                otp_entry = PasswordResetOTP.objects.get(otp=otp, is_used=False)
                
                # Expiry check
                if timezone.now() > otp_entry.created_at + timedelta(minutes=10):
                    return Response({'message': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update password
                user = otp_entry.user
                user.set_password(new_password)
                user.save()

                # Delete OTP entry
                otp_entry.delete()

            except PasswordResetOTP.DoesNotExist:
                return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)       

        return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)