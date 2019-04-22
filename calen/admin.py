from django.contrib import admin

from .models import Event, PendingEvent, Invite

# Register your models here.

admin.site.register(Event)
admin.site.register(PendingEvent)
admin.site.register(Invite)