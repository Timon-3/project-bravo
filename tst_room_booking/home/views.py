from django.shortcuts import render, redirect
from home.models import Room, Event
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from home.forms import EventForm, FilterForm, RegisterUserForm
from datetime import date, datetime
from home.utils import formatcal
from django.utils.safestring import mark_safe

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


def roomdetail(request, room_id):
"""<<<<<<< add_calendar_view
    form = EventForm(request.POST or None)
    html_cal = formatcal(room_id)
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
                Eventf.save()
                form = EventForm()
    html_cal = formatcal(room_id)
    cal = mark_safe(html_cal)
    room_list = Event.objects.filter(room=room_id)
    room = Room.objects.get(id=room_id)
    return render(request, "home/room.html", {"room": room, "form": form, "room_list": room_list, "cal": cal})
"""

    if request.user.is_authenticated:

        form = EventForm(request.POST or None)
        html_cal = formatcal(room_id)
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
        html_cal = formatcal(room_id)
        cal = mark_safe(html_cal) 
        room_list = Event.objects.filter(room=room_id)
        room = Room.objects.get(id=room_id)
        return render(request, "home/room.html", {"room": room, "form": form, "room_list": room_list, "cal": cal})
    else:
        return redirect('/login')

def secured(request):
    if request.user.is_authenticated:
            return render(request, 'home/secured.html', {})
    return redirect('/login')
