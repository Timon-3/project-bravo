from django.shortcuts import render
from home.models import Room
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView


# Create your views here.

def home(request):
    return render(request, "home/home.html")


@login_required(login_url="/admin")
def secured(request):
    return render(request, 'home/secured.html', {})


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