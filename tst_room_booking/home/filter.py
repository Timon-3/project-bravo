import django_filters
from django.forms import DateInput
from django_filters import *
from home.models import Event

class Event_Filter(django_filters.FilterSet):
    class Meta:
        model=Event
        widgets = {
        }
        fields=['description']