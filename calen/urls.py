from django.urls import path

from .eventviews import CreateEvent, CreateEventGen, ListEvents, TestEvent, CreatePE, ShowInvites, AcceptInvite, ShowPMSatus, AvailableSlots

from .useriviews import Home, CreateUser, LoginView, Welcome

from .nlpviews import Talk

from rest_framework.authtoken.views import obtain_auth_token

from django.views.generic.base import TemplateView

urlpatterns = [
    #path('', Welcome.as_view(), name= "welcome"),
    path('', TemplateView.as_view(template_name='home.html'), name='welcom'),
    path('signup/', CreateUser.as_view(), name= 'make_user'),
    path('login/', LoginView.as_view(), name= "login_view"),
    path('home/', Home.as_view(), name= "who_am_i"),

    path('me/', CreateEvent.as_view(), name= 'make_event'),
    path('mpe/', CreatePE.as_view(), name= 'make_pending_event'),
    path('meg/', CreateEventGen.as_view(), name= 'make_event_gen'),
    path('le/', ListEvents.as_view(), name= "list_evens"),
    path('te/', TestEvent.as_view(), name= "test_event"),
    path('si/', ShowInvites.as_view(), name= 'show_invites'),
    path('ai/', AcceptInvite.as_view(), name= 'accept_invite'),
    path('spes/', ShowPMSatus.as_view(), name= 'show_pe_status'),
    #path('llogin/', obtain_auth_token, name= "llogin_view"),

    path('as/', AvailableSlots.as_view(), name= 'availabel_slots'),

    path('bot/', Talk.as_view(), name= 'talk'),
]
