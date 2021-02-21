import datetime
import json
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, View
from django.views.generic.edit import FormMixin
from .models import Event, EventMember
from .forms import AddEventMemberForm, EventForm
from user.models import User


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
        slot = request.POST.get("slot", None)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)

        start = f"{date} {start_time}"
        end = f"{date} {end_time}"

        start_object = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
        end_object = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")

        event = Event(name=str(name), start=start_object, end=end_object, slot=slot)
        event.save()

        return redirect("event:event_calendar")


class EventView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)

        is_registered = event.eventmember_set.filter(user_id=request.user.pk).exists()
        return render(
            request,
            "event/event_detail.html",
            {
                "form": AddEventMemberForm(),
                "event": event,
                "is_registered": is_registered,
            },
        )


class RegisterForEvent(View):
    def post(self, request):

        event_id = request.POST.get("event", None)
        user_id = request.POST.get("user", None)

        event = Event.objects.get(pk=event_id)
        user = User.objects.get(pk=user_id)

        inscription = EventMember(event=event, user=user)
        inscription.save()

        event.reserved_slot += 1
        event.save()

        return redirect("event:event_calendar")


class UnsubscribeFromEvent(View):
    def post(self, request):

        event_id = request.POST.get("event", None)
        user_id = request.POST.get("user", None)

        event = Event.objects.get(pk=event_id)

        user = User.objects.get(pk=user_id)

        inscription = EventMember.objects.get(event=event, user=user)
        inscription.delete()

        event.reserved_slot -= 1
        event.save()

        return redirect("event:event_calendar")
