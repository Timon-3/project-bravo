from django.urls import path
from home import views
from home.models import Room

home_list_view = views.HomeListView.as_view(queryset = Room.objects.all()[:5], # :5 limits the results to the five most recent
context_object_name="room_list",
template_name="home/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("secured", views.secured)
]