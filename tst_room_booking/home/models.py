from django.db import models
from datetime import timezone
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(default=0)
    description = models.CharField(max_length=2000)
    image = models.ImageField(default=None)
    chairs = models.IntegerField(default=0)
    tables = models.IntegerField(default=0)
    beamer = models.IntegerField(default=0)
    video = models.BooleanField(default=False)
    ethernet = models.BooleanField(default=False)
    wlan = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return self.description

    