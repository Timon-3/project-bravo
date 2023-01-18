from django.shortcuts import render
from home.models import Room
from django.views.generic import ListView
from home.forms import EventForm
# Create your views here.

# Create your views here.
class HomeListView(ListView):
    """Renders the home page, with a list of all Rooms"""
    model = Room
    def get_context_data(self, **kwargs):
        context = super(HomeListView, 
        self).get_context_data(**kwargs)
        return context

def roomdetail(request, room_id):
    form = EventForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            Event = form.save(commit=False)
            Event.save()
    room = Room.objects.get(id=room_id)
    return render(request, "home/room.html", {"room": room, "form": form})