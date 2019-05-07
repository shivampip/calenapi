from django.urls import path

from .eventviews import  ListEvents, CreatePE, ShowInvites, AcceptInvite, ShowPMSatus, AvailableSlots, CreateBusySlot, CreateBusySlots, GetBusySlot

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

    path('mpe/', CreatePE.as_view(), name= 'make_pending_event'),
    path('le/', ListEvents.as_view(), name= "list_evens"),
    path('si/', ShowInvites.as_view(), name= 'show_invites'),
    path('ai', AcceptInvite.as_view(), name= 'accept_invite'),
    path('spes/', ShowPMSatus.as_view(), name= 'show_pe_status'),
    #path('llogin/', obtain_auth_token, name= "llogin_view"),
    path('bs/', CreateBusySlot.as_view(), name= "busy_slot"),
    path('bss/', CreateBusySlots.as_view(), name= "busy_slots"),
    path('getbs/', GetBusySlot.as_view(), name= "get_busy_slots"),

    path('as/', AvailableSlots.as_view(), name= 'availabel_slots'),

    #path('bot/', Talk.as_view(), name= 'talk'),
]
