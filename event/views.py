from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class EventView(View):
    # template_name = "event/event_calendar.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "event/event_calendar.html")
