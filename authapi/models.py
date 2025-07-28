from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Override 'email' field to make it required and unique
    email = models.EmailField(unique=True)

    # Optional: Add your own fields
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
