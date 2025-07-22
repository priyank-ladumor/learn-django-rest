from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    role_number = models.IntegerField(unique=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.name}"
