#dio koda preuzet sa https://youtu.be/WuyKxdLcw3w

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description

class UserAction(models.Model):
    ACTION_TYPES = (
        ('POST', 'User created a post'),
        ('DELETE', 'User deleted a post by user'),
        ('BANNED', 'User banned user'),
        ('UNBANNED', 'User unbanned user'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=12, choices=ACTION_TYPES)
    target_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='targeted_actions')
    target_post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)
    deleted_post_author = models.CharField(max_length=150, null=True, blank=True)  # novo polje za spremanje imena autora izbrisanog posta
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.action_type == 'POST':
            return f"User {self.user.username} created a post at {self.timestamp}"
        elif self.action_type == 'DELETE':
            return f"User {self.user.username} deleted a post by {self.deleted_post_author} at {self.timestamp}"  # koristimo deleted_post_author umjesto self.target_post.author.username
        elif self.action_type == 'BANNED':
            return f"User {self.user.username} banned user {self.target_user.username} at {self.timestamp}"
        elif self.action_type == 'UNBANNED':
            return f"User {self.user.username} unbanned user {self.target_user.username} at {self.timestamp}"