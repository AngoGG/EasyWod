from django.contrib import admin

from .models import Event, EventMember

# Register your models here.

admin.site.register(Event)
admin.site.register(EventMember)
