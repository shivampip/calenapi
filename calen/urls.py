from django.urls import path

from .apiviews import CreatePerson, CreateEvent, CreateEventGen, CreateUser, LoginView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('makeperson/', CreatePerson.as_view(), name= 'make_person'),
    path('makeevent/', CreateEvent.as_view(), name= 'make_event'),
    path('makeeventgen/', CreateEventGen.as_view(), name= 'make_event_gen'),
    path('users/', CreateUser.as_view(), name= 'make_user'),
    path('login/', LoginView.as_view(), name= "login_view"),
    #path('llogin/', obtain_auth_token, name= "llogin_view"),
]
