from django.shortcuts import render, redirect, get_object_or_404
from home.models import Room, Event
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from home.forms import EventForm, FilterForm, RegisterUserForm, ModifyForm
from datetime import date, datetime, timedelta
from home.utils import formatcal
from django.utils.safestring import mark_safe
from rest_framework import permissions
from home.serializers import EventSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User 
from django.http import HttpResponseRedirect
from django.urls import reverse


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

def add(d):
    d = datetime.strptime(d,"%Y-%d-%m")
    d = d + timedelta(days=7)
    d = d.strftime("%Y-%d-%m")
    return "d=" + d

def dect(d):
    d = datetime.strptime(d,"%Y-%d-%m")
    d = d - timedelta(days=7)
    d = d.strftime("%Y-%d-%m")
    return "d=" + d

def get_date(d):
    if d:
        return d
    return date.today().strftime("%Y-%d-%m")

class EventDeleteView(DeleteView):
    model = Event
    success_url = '/secured'
    template_name = "home/delete.html"

    # make sure only users who are logged in can access the delete event page
    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect("/login")
        return super().get(request, *args, **kwargs)


def roomdetail(request, room_id):
    form = EventForm(request.POST or None)
    d = get_date(request.GET.get('d', None))
    add_cal = add(d)
    dect_cal = dect(d)
    if request.user.is_authenticated:
        form = EventForm(request.POST or None)
        html_cal = formatcal(room_id, d, False)
        cal = mark_safe(html_cal)
        if request.method == "POST":
            if form.is_valid():
                Room_id = request.POST.get("room")
                starttime = request.POST.get("start_time")
                endtime = request.POST.get("end_time")
                description = request.POST.get("description")
                Event_overlapping_start = Event.objects.filter(room=Room_id, start_time__gt=starttime, start_time__lt=endtime).exists()
                Event_overlapping_end = Event.objects.filter(room=Room_id, end_time__gt=starttime, end_time__lt=endtime).exists()
                # check for items that envelope this item
                Event_enveloping = Event.objects.filter(room=Room_id, start_time__lt=starttime, end_time__gt=endtime).exists()
                Event_overlapping_start_end = Event.objects.filter(room=Room_id, start_time=starttime, end_time=endtime).exists()
                Event_items_present = Event_overlapping_start or Event_overlapping_end or Event_enveloping or Event_overlapping_start_end
                startdatetime = datetime.strptime(starttime,'%Y-%m-%dT%H:%M')
                enddatetime = datetime.strptime(endtime,'%Y-%m-%dT%H:%M')
                if startdatetime > enddatetime:
                    room = Room.objects.get(id=room_id)
                    conflict = ("Starttime has to be before the Endtime")
                    return render(request, "home/room.html", {"room": room, "form": form, "conflict": conflict, "cal": cal, "add_cal": add_cal, "dect_cal": dect_cal})
                if Event_items_present:
                    room = Room.objects.get(id=room_id)
                    conflict = (f"{room} is already booked at this time")
                    return render(request, "home/room.html", {"room": room, "form": form, "conflict": conflict, "cal": cal, "add_cal": add_cal, "dect_cal": dect_cal})
                elif startdatetime.day != enddatetime.day:
                    endtime = datetime.strftime(datetime(year=startdatetime.year,month=startdatetime.month,day=startdatetime.day,hour=19,minute=0),'%Y-%m-%dT%H:%M')
                    Eventf = form.save(commit=False)
                    Eventf.user = request.user
                    Eventf.end_time = endtime
                    Room_id = Eventf.room
                    Eventf.save()
                    form = EventForm()
                    while startdatetime.day != enddatetime.day:
                        startdatetime = startdatetime + timedelta(days=1)
                        starttime = datetime.strftime(datetime(year=startdatetime.year,month=startdatetime.month,day=startdatetime.day,hour=7,minute=0),'%Y-%m-%dT%H:%M')
                        if startdatetime.day == enddatetime.day:
                            endtime = datetime.strftime(datetime(year=enddatetime.year,month=enddatetime.month,day=enddatetime.day,hour=enddatetime.hour,minute=enddatetime.minute),'%Y-%m-%dT%H:%M')
                        else:
                            endtime = datetime.strftime(datetime(year=startdatetime.year,month=startdatetime.month,day=startdatetime.day,hour=19,minute=0),'%Y-%m-%dT%H:%M')
                        Eventf = form.save(commit=False)
                        Eventf.user = request.user
                        Eventf.room = Room_id
                        Eventf.end_time = endtime
                        Eventf.start_time = starttime
                        Eventf.description = description
                        Eventf.save()
                        form = EventForm()
                else:
                    Eventf = form.save(commit=False)
                    Eventf.user = request.user
                    Eventf.save()
                    form = EventForm()
        html_cal = formatcal(room_id, d, False)
        cal = mark_safe(html_cal) 
        room_list = Event.objects.filter(room=room_id)
        room = Room.objects.get(id=room_id)
        return render(request, "home/room.html", {"room": room, "form": form, "room_list": room_list, "cal": cal, "add_cal": add_cal, "dect_cal": dect_cal})

    if request.user.is_authenticated == False:
        html_cal = formatcal(room_id, d, True)

    else:
        html_cal = formatcal(room_id, d, False)

    cal = mark_safe(html_cal) 
    room_list = Event.objects.filter(room=room_id)
    room = Room.objects.get(id=room_id)

    return render(request, "home/room.html", {"room": room, "form": form, "room_list": room_list, "cal": cal, "add_cal": add_cal, "dect_cal": dect_cal})


def secured(request):
    if request.user.is_authenticated:
        date_format = "%d.%m.%Y %H:%M"

        event_list = Event.objects.none()
        events_list = Event.objects.all()
        user_events = []  # -> free_room
        for event in events_list:
            if event.user == request.user:
                user_events.append(event.pk)
        for id in user_events:
            event = Event.objects.filter(id=id)
            event_list = event_list | event
        return render(request, "home/secured.html", {"event_list": event_list})
    else:
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


def modify(request, event_id=None):
    if request.user.is_authenticated:
        instance = Event()
        if event_id:
            instance = get_object_or_404(Event, pk=event_id)
        else:
            instance = Event()
        event_id = event_id
        form = ModifyForm(request.POST or None, instance=instance)
        if request.POST and form.is_valid():
            Room_id = request.POST.get("room")
            starttime = request.POST.get("start_time")
            endtime = request.POST.get("end_time")
            Event_overlapping_start = Event.objects.filter(room=Room_id, start_time__gt=starttime, start_time__lt=endtime).exclude(id=event_id).exists()
            Event_overlapping_end = Event.objects.filter(room=Room_id, end_time__gt=starttime, end_time__lt=endtime).exclude(id=event_id).exists()
            # check for items that envelope this item
            Event_enveloping = Event.objects.filter(room=Room_id, start_time__lt=starttime, end_time__gt=endtime).exclude(id=event_id).exists()
            Event_overlapping_start_end = Event.objects.filter(room=Room_id, start_time=starttime, end_time=endtime).exclude(id=event_id).exists()
            Event_items_present = Event_overlapping_start or Event_overlapping_end or Event_enveloping or Event_overlapping_start_end
            if Event_items_present:
                room = Room.objects.get(id=Room_id)
                conflict = (f"you can't modify this event the {room} is already booked at this time")
                return render(request, "home/modify.html", {"form": form, "conflict": conflict})
            else:
                form.save()
                return HttpResponseRedirect(reverse('secured'))
        return render(request, 'home/modify.html', {'form': form})
    else:
        return redirect('/login')