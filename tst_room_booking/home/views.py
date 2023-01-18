from django.shortcuts import render
from home.models import Room
from django.views.generic import ListView

# Create your views here.

def home(request):
    return render(request, "home/home.html")

# Create your views here.
class HomeListView(ListView):
    """Renders the home page, with a list of all Rooms"""
    model = Room
    def get_context_data(self, **kwargs):
        context = super(HomeListView, 
        self).get_context_data(**kwargs)
        return context
