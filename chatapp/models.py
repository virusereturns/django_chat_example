from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'slug': self.slug})


class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "Chat Messages"
