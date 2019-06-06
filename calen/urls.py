from django.urls import path

from .eventviews import  ListEvents, CreatePE, ShowInvites, AcceptInvite, ShowPMSatus, AvailableSlots, CreateBusySlots, GetBusySlot, CreateAASlots, GetAASlot, DaySchedule, GetShareableLink, BrowseLink, GetBestAvailableSlot, GetNotifications

from .useriviews import Verify, Register, GetToken

from rest_framework.authtoken.views import obtain_auth_token

from django.views.generic.base import TemplateView

urlpatterns = [
    #path('', Welcome.as_view(), name= "welcome"),
    path('', TemplateView.as_view(template_name='home.html'), name='welcom'),

    path('register/', Register.as_view(), name= 'make_user'),
    path('get_token/', GetToken.as_view(), name= "login_view"),
    path('verify/', Verify.as_view(), name= "verify"),

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
    path('get_best_available_slots/', GetBestAvailableSlot.as_view(), name= 'best_availabel_slots'),

    path('get_day_schedule/', DaySchedule.as_view(), name= "get_schedule"),

    path('get_shareable_link/', GetShareableLink.as_view(), name= "shareable_link"),

    path('browse/', BrowseLink.as_view(), name= "browse_link"),

    path('notifications/', GetNotifications.as_view(), name= "get_notifications")

]
