from django.shortcuts import render, redirect
from home.models import Room, Event
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from home.forms import EventForm, FilterForm, RegisterUserForm
from datetime import date, datetime
from home.utils import formatcal
from django.utils.safestring import mark_safe
from rest_framework import permissions
from home.serializers import EventSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User 

# Create your views here.
class HomeListView(ListView):
    """Renders the home page, with a list of all Rooms"""
    model = Room
    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def search(request):
    form = FilterForm(request.POST or None)
    #room_list = []
    room_list = Event.objects.none()
    free_room = []
    if request.method == "POST":
        starttime = request.POST.get("start_time")
        endtime = request.POST.get("end_time")
        rooms_list = Room.objects.all()
        for room in rooms_list:
            Event_overlapping_start = Event.objects.filter(room=room.pk, start_time__gte=starttime, start_time__lt=endtime).exists()
            Event_overlapping_end = Event.objects.filter(room=room.pk, end_time__gt=starttime, end_time__lte=endtime).exists()
            # check for items that envelope this item
            Event_enveloping = Event.objects.filter(room=room.pk, start_time__lte=starttime, end_time__gte=endtime).exists()
            Event_items_present = Event_overlapping_start or Event_overlapping_end or Event_enveloping

            if Event_items_present:
                continue
            else:
                free_room.append(room.pk)
        print(free_room,"1")
        for id in free_room:
            room = Room.objects.filter(id=id)
            room_list = room_list | room
        form = FilterForm()
    return render(request, "home/search.html", {"form": form, "room_list": room_list})


class LoginInterfaceView(SuccessMessageMixin, LoginView):
    template_name = "home/login.html"
    success_message = "You successfully logged in"


class LogoutInterfaceView(SuccessMessageMixin, LogoutView):
    template_name = "home/logout.html"
    success_message = "Your logout was successful. Have a great day =)"


class SignupView(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "home/register.html"
    success_url = "/secured"
    success_message = "Welcome! You successfully signup."

    # make sure only users who are not already logged in can access the signup page
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/secured")
        return super().get(request, *args, **kwargs)


class EventDeleteView(DeleteView):
    model = Event
    success_url = '/secured'
    template_name = "home/delete.html"


def roomdetail(request, room_id):
    form = EventForm(request.POST or None)

    if request.user.is_authenticated:
        html_cal = formatcal(room_id, False)
        cal = mark_safe(html_cal)
        if request.method == "POST":
            if form.is_valid():
                Room_id = request.POST.get("room")
                starttime = request.POST.get("start_time")
                endtime = request.POST.get("end_time")
                Event_overlapping_start = Event.objects.filter(room=Room_id, start_time__gt=starttime, start_time__lt=endtime).exists()
                Event_overlapping_end = Event.objects.filter(room=Room_id, end_time__gt=starttime, end_time__lt=endtime).exists()
                # check for items that envelope this item
                Event_enveloping = Event.objects.filter(room=Room_id, start_time__lt=starttime, end_time__gt=endtime).exists()
                Event_items_present = Event_overlapping_start or Event_overlapping_end or Event_enveloping

                if Event_items_present:
                    room = Room.objects.get(id=room_id)
                    conflict = (f"{room} is already booked at this time")
                    return render(request, "home/room.html", {"room": room, "form": form, "conflict": conflict, "cal": cal})
                else:
                    Eventf = form.save(commit=False)
                    Eventf.user = request.user
                    Eventf.save()
                    form = EventForm()

    if request.user.is_authenticated == False:
        html_cal = formatcal(room_id, True)
    else:
        html_cal = formatcal(room_id, False)

    cal = mark_safe(html_cal) 
    room_list = Event.objects.filter(room=room_id)
    room = Room.objects.get(id=room_id)

    return render(request, "home/room.html", {"room": room, "form": form, "room_list": room_list, "cal": cal})


def secured(request):
    if request.user.is_authenticated:

        event_list = Event.objects.none()
        events_list = Event.objects.all()
        user_events = []  # -> free_room
        for event in events_list:
            if event.user == request.user:
                user_events.append(event.pk)
        print(user_events,"1")
        for id in user_events:
            event = Event.objects.filter(id=id)
            print("event: ",event)
            event_list = event_list | event
        return render(request, "home/secured.html", {"event_list": event_list})

        # return render(request, 'home/secured.html', {})
    return redirect('/login')

class EventListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, room_id):
        '''
        Helper method to get the Events with given room_id
        '''
        try:
            return Event.objects.filter(room=room_id)
        except Event.DoesNotExist:
            return None

    def get(self, request, room_id, *args, **kwargs):
        '''
        Retrieves the Events with given room_id
        '''
        event_instance = self.get_object(room_id)
        if not event_instance:
            return Response(
                {"res": "Events with room_id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EventSerializer(event_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)