from django.urls import path

from .eventviews import CreateEvent, CreateEventGen, ListEvents, TestEvent, CreatePE

from .useriviews import Home, CreateUser, LoginView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup/', CreateUser.as_view(), name= 'make_user'),
    path('login/', LoginView.as_view(), name= "login_view"),
    path('home/', Home.as_view(), name= "who_am_i"),

    path('me/', CreateEvent.as_view(), name= 'make_event'),
    path('mpe/', CreatePE.as_view(), name= 'make_pending_event'),
    path('meg/', CreateEventGen.as_view(), name= 'make_event_gen'),
    path('le/', ListEvents.as_view(), name= "list_evens"),
    path('te/', TestEvent.as_view(), name= "test_event"),
    #path('llogin/', obtain_auth_token, name= "llogin_view"),
]
