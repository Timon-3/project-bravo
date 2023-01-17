from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    description = models.CharField(max_length=2000)
    