from rest_framework import serializers
from django.contrib.auth.models import User

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