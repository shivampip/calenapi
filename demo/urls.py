from django.urls import path

from . import views 

urlpatterns = [
    path('index/', views.index),        #Done
    path('login/', views.login),        #Done
    path('register/', views.register),  #Done
    path('home/', views.home),          #Done
    path('test/', views.test),

    path('CreateEvent/', views.create_event),                         #Done
    path('CreatePendingEvent/', views.create_pending_event),          #Done
    path('ListEvent/', views.list_event),
    path('ShowPendingEventStatus/', views.show_pending_event_status),

    path('ShowInvites/', views.show_invites),
    path('AcceptInvites/', views.accept_invite),

    path('talk', views.talk),
]

    

