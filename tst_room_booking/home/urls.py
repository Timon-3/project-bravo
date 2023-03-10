from django.urls import path
from home import views
from home.models import Room, Event

home_list_view = views.HomeListView.as_view(queryset = Room.objects.all()[:5], # :5 limits the results to the five most recent
context_object_name="room_list",
template_name="home/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("room/<room_id>/", views.roomdetail, name="room"),
    path("search", views.search, name="search"),
    path("secured", views.secured, name="secured"),
    path("<pk>/delete", views.EventDeleteView.as_view(), name="delete"),
    path("login", views.LoginInterfaceView.as_view(), name="login"),
    path("logout", views.LogoutInterfaceView.as_view(), name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path('api', views.EventListApiView.as_view()),
    path('api/<int:room_id>/', views.EventDetailApiView.as_view()),
    path('api/user', views.UserListApiView.as_view()),
    path('api/room', views.RoomListApiView.as_view()),
    path('modify/<event_id>/', views.modify, name='modify')
]
