from django.db import models
from django.utils import timezone

class Blogs(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class Comments(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    
    def __str__(self):
        return f'{self.comment} - {self.blog.title}'