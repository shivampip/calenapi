from django.urls import path

from .eventviews import  ListEvents, CreatePE, ShowInvites, AcceptInvite, ShowPMSatus, AvailableSlots, CreateBusySlots, GetBusySlot, CreateAASlots, GetAASlot

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

    path('make_pending_event/', CreatePE.as_view(), name= 'make_pending_event'),
    path('show_pending_event_status/', ShowPMSatus.as_view(), name= 'show_pe_status'),
    path('list_events/', ListEvents.as_view(), name= "list_evens"),

    path('show_invites/', ShowInvites.as_view(), name= 'show_invites'),
    path('accept_invite/', AcceptInvite.as_view(), name= 'accept_invite'),
    
    path('make_busy_slots/', CreateBusySlots.as_view(), name= "busy_slots"),
    path('get_busy_slots/', GetBusySlot.as_view(), name= "get_busy_slots"),

    path('make_aa_slots/', CreateAASlots.as_view(), name= "always_available_slots"),
    path('get_aa_slots/', GetAASlot.as_view(), name= "get_always_available_slots"),
    
    path('get_available_slots/', AvailableSlots.as_view(), name= 'availabel_slots'),

]
