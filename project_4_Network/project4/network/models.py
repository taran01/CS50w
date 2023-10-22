from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField("Post", related_name="user_likes", null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(validators=[MinValueValidator(limit_value=0)], default=0)

    def __str__(self):
        return f"{self.user}'s post"

class Followers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="following")

    def __str__(self):
        return f"{self.user}"
