from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
import uuid


class CustomUser(AbstractUser):
    # Override 'email' field to make it required and unique
    email = models.EmailField(unique=True)

    # Optional: Add your own fields
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

User = get_user_model()
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"
