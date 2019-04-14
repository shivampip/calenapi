from django.contrib import admin

from .models import Person, Event

# Register your models here.

admin.site.register(Person)
admin.site.register(Event)