from django.db import models
from datetime import timezone
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    description = models.CharField(max_length=2000)
    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return str(self.room)

    def save(self, *args, **kwargs):
        # check for items that have an overlapping start date
        Event_overlapping_start = Event.objects.filter(start_time__gte=self.start_time, start_time__lte=self.end_time).exists()
        # check for items that have an overlapping end date
        Event_overlapping_end = Event.objects.filter(end_time__gte=self.start_time, end_time__lte=self.end_time).exists()
        # check for items that envelope this item
        Event_enveloping = Event.objects.filter(start_time__lte=self.start_time, end_time__gte=self.end_time).exists()
        Event_items_present = Event_overlapping_start or Event_overlapping_end or Event_enveloping

        if Event_items_present:
            return 
        else:
            super(Event, self).save(*args, **kwargs) # Call the "real" save() method.
