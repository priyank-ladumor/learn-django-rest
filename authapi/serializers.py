from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ( 'username', 'email')
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer): # ModelSerializer Use when we need class meta 
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # fields = '__all__'
        
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
        
class LoginSerializer(serializers.Serializer): # Serializer Use when we don't need class meta
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']  
        
        
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class VerifyOTPAndChangePasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(max_length=128, required=True)

class ChangePasswordViewSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)