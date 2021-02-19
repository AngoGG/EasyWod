import datetime
import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Event


class CalendarView(ListView):
    def get(self, request):
        all_events = Event.objects.all()
        context = {
            "events": all_events,
        }
        return render(request, "event/event_calendar.html", context)

