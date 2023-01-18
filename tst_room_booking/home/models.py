from django.db import models
from datetime import timezone

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    description = models.CharField(max_length=2000)
    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=2000)
    def __str__(self) -> str:
        return self.description