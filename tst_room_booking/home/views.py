from django.shortcuts import render, redirect
from home.models import Room, Event
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from home.forms import EventForm
from datetime import date


# Create your views here.
class HomeListView(ListView):
    """Renders the home page, with a list of all Rooms"""
    model = Room
    def get_context_data(self, **kwargs):
        context = super(HomeListView, 
        self).get_context_data(**kwargs)
        return context


class LoginInterfaceView(LoginView):
    template_name = "home/login.html"

class LogoutInterfaceView(LogoutView):
    template_name = "home/logout.html"

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "home/register.html"
    success_url = "/secured"

    # make sure only users who are not already logged in can access the signup page
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/secured")
        return super().get(request, *args, **kwargs)


def roomdetail(request, room_id):
    form = EventForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            Room_id = request.POST.get("room")
            starttime = request.POST.get("start_time")
            endtime = request.POST.get("end_time")
            Event_overlapping_start = Event.objects.filter(room=Room_id, start_time__gt=starttime, start_time__lt=endtime).exists()
            Event_overlapping_end = Event.objects.filter(end_time__gt=starttime, end_time__lt=endtime).exists()
            # check for items that envelope this item
            Event_enveloping = Event.objects.filter(start_time__lt=starttime, end_time__gt=endtime).exists()
            Event_items_present = Event_overlapping_start or Event_overlapping_end or Event_enveloping

            if Event_items_present:
                print("conflict")
                conflict = ("Your Room is already Booked")
                room = Room.objects.get(id=room_id)
                return render(request, "home/room.html", {"room": room, "form": form, "conflict": conflict})
            else:
                Eventf = form.save(commit=False)
                Eventf.save()
                form = EventForm()
            
    room = Room.objects.get(id=room_id)
    return render(request, "home/room.html", {"room": room, "form": form})

def secured(request):
    if request.user.is_authenticated:
            return render(request, 'home/secured.html', {})
    return redirect('/login')
