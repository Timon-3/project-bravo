from home.models import Event
from rest_framework import serializers
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    room = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = ['room', 'user', 'start_time', 'end_time', 'description']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')