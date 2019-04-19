from django.urls import path

from .apiviews import CreateEvent, CreateEventGen, CreateUser, LoginView, ListEvents

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('makeevent/', CreateEvent.as_view(), name= 'make_event'),
    path('makeeventgen/', CreateEventGen.as_view(), name= 'make_event_gen'),
    path('listevents/', ListEvents.as_view(), name= "list_evens"),
    path('users/', CreateUser.as_view(), name= 'make_user'),
    path('login/', LoginView.as_view(), name= "login_view"),
    #path('llogin/', obtain_auth_token, name= "llogin_view"),
]
