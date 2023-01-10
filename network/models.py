from django.contrib.auth.models import AbstractUser
from django.db import models

# User model.


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
        }

    def __str__(self):
        return self.username

# Post model that has info about the post.


class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=255)
    likes = models.ManyToManyField(
        'User', default=None, blank=True, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
            "userId": self.user.id,
            "username": self.user.username,
            "likes": self.likes.all().count()
        }

# Profile model that stores information about the profile of each user.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        "User", blank=True, null=True, related_name="Following")
    followers = models.ManyToManyField(
        "User", blank=True, null=True, related_name="Followers")
