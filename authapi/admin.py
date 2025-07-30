from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import PasswordResetOTP
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    
@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'created_at', 'is_used']  