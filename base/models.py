
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True)
    bio = models.TextField(max_length=255, null=True)
    avatar = models.ImageField(null = True, default='avatar.svg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Media(models.Model):
    user = models.ForeignKey(User, related_name='media', on_delete=models.CASCADE, null=True)
    room = models.ForeignKey('Room', related_name='media', on_delete=models.CASCADE, null=True)
    file = models.FileField()

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =['-updatedAt', '-createdAt']

    def __str__(self):
        return self.body[0:50]
    

class Room(models.Model):
    host = models.ForeignKey(User, related_name='rooms', on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, related_name='rooms', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True , null=True)
    participants = models.ManyToManyField(User, related_name="participants")
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-updatedAt', '-createdAt']

    def __str__(self):
        return self.name

