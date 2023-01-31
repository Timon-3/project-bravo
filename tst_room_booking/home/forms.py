from django import forms
from django.forms import DateInput
from home.models import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# add extra fields to django's user form
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
        'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('room', 'description', 'start_time', 'end_time')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class FilterForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
        'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields=["start_time","end_time"]

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)