from django.contrib import admin

from .models import Event, PendingEvent, Invite, BusySlot, AASlot, Notification

# Register your models here.

admin.site.register(Event)
admin.site.register(PendingEvent)
admin.site.register(Invite)
admin.site.register(BusySlot)
admin.site.register(AASlot) 
admin.site.register(Notification)