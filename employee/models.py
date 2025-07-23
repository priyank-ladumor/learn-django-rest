from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name} - {self.designation}'