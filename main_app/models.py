from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country_born = models.CharField(max_length=100)
    countries_lived = models.TextField()
    current_country = models.CharField(max_length=100)

    def __str__(self):
        return self.name or self.user.username
    
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'user_id': self.user.id})

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    tags = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.id})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.post.title}'