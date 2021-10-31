from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatar.png')

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-user']


class Room(models.Model):
    title = models.CharField(max_length=127, unique=True)
    description = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='own_rooms')
    members = models.ManyToManyField(Account, related_name='rooms')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/chat/{self.id}'

    class Meta:
        ordering = ['-title']


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created_at']
