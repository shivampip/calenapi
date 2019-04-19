from django.urls import path

from .apiviews import CreatePerson, CreateEvent, CreateEventGen, CreateUser

urlpatterns = [
    path('makeperson/', CreatePerson.as_view(), name= 'make_person'),
    path('makeevent/', CreateEvent.as_view(), name= 'make_event'),
    path('makeeventgen/', CreateEventGen.as_view(), name= 'make_event_gen'),
    path('users/', CreateUser.as_view(), name= 'make_user'),
]
