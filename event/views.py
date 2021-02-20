import datetime
import json
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, View
from .models import Event
from .forms import EventForm


class CalendarView(ListView):
    context_object_name = "events"
    queryset = Event.objects.all()
    template_name = "event/event_calendar.html"


class AddEvent(UserPassesTestMixin, View):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "event/add_event.html", {"form": EventForm()})

    def post(self, request):

        name = request.POST.get("name", None)
        date = request.POST.get("date", None)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)

        start = f"{date} {start_time}"
        end = f"{date} {end_time}"

        start_object = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
        end_object = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")

        event = Event(name=str(name), start=start_object, end=end_object)
        event.save()

        return redirect("event:event_calendar")
