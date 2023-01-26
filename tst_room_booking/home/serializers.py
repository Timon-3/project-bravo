from home.models import Event
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['room', 'user', 'start_time', 'end_time', 'description']