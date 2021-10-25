from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatar.png')
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Room(models.Model):
    title = models.CharField(max_length=127, unique=True)
    description = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(UserProfile, blank=True, related_name='rooms')
    own = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/chat/{self.id}'


class Message(models.Model):
    content = models.TextField(max_length=900)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created_at']
