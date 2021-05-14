from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView, View

from membership.models import Membership, UserMembership
from user.models import User

from .forms import AddEventMemberForm, EventForm
from .models import Event, EventMember


class CalendarView(ListView):
    def get(self, request):
        event_list = Event.objects.all()
        time = datetime.now()
        # If User if employee, just send event list and time

        if self.request.user.is_authenticated and self.request.user.type != "EMPLOYEE":
            user_membership = (
                self.request.user.user_membership.membership.membership_type
            )
            # If User if on trial memberbership, get his trial remaining events and the events in which he participated
            if user_membership == "TRIAL":

                user_remaining_courses = (
                    self.request.user.user_membership.remaining_trial_courses
                )

                return render(
                    request,
                    "event/event_calendar.html",
                    {
                        "events": event_list,
                        "time": time,
                        "user_remaining_courses": user_remaining_courses,
                    },
                )
            # Else, juste returns the time and all user events
            else:
                return render(
                    request,
                    "event/event_calendar.html",
                    {"events": event_list, "time": time},
                )
        return render(
            request, "event/event_calendar.html", {"events": event_list, "time": time,},
        )


class AddEvent(UserPassesTestMixin, View):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "event/add_event.html", {"form": EventForm()})

    def post(self, request):

        name = request.POST.get("name", None)
        date = request.POST.get("date", None)
        slot = request.POST.get("slot", 5)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)

        start = f"{date} {start_time}"
        end = f"{date} {end_time}"

        start_object = datetime.strptime(start, "%Y-%m-%d %H:%M")
        end_object = datetime.strptime(end, "%Y-%m-%d %H:%M")

        # frequency calcul

        if request.POST.get("frequency", None) == 'daily':
            interval = 1
            frequency = 7
        elif request.POST.get("frequency", None) == 'weekly':
            interval = 7
            frequency = 1
        else:
            frequency = False
        if frequency:
            period = int(request.POST.get("period", "1"))
            for week in range(period):
                for day in range(frequency):
                    event = Event(
                        name=str(name), start=start_object, end=end_object, slot=slot
                    )
                    event.save()
                    start_object += timedelta(days=interval)
                    end_object += timedelta(days=interval)
        else:
            event = Event(name=str(name), start=start_object, end=end_object, slot=slot)
            event.save()

        return redirect("event:event_calendar")


class EventView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        time = datetime.now()

        is_registered = event.eventmember_set.filter(user_id=request.user.pk).exists()
        if is_registered:
            registration = event.eventmember_set.get(
                user_id=request.user.pk, event_id=event.pk
            )
            has_cancelled = False if registration.date_cancellation is None else True
        else:
            has_cancelled = False
        if self.request.user.is_authenticated and self.request.user.type != "EMPLOYEE":
            user_membership = (
                self.request.user.user_membership.membership.membership_type
            )
            if user_membership == "TRIAL":
                user_events = EventMember.objects.filter(
                    user=self.request.user, date_cancellation__isnull=True
                ).count()
                user_remaining_courses = (
                    Membership.objects.get(membership_type="TRIAL").trial_courses
                    - user_events
                )
                return render(
                    request,
                    "event/event_detail.html",
                    {
                        "form": AddEventMemberForm(),
                        "event": event,
                        "is_registered": is_registered,
                        "has_cancelled": has_cancelled,
                        "user_remaining_courses": user_remaining_courses,
                        "active_membership": self.request.user.user_membership.active,
                        "time": time,
                    },
                )
            # If User if on Premium memberbership, check if his subscribtion is active
            elif user_membership == "PREMIUM":
                return render(
                    request,
                    "event/event_detail.html",
                    {
                        "form": AddEventMemberForm(),
                        "event": event,
                        "is_registered": is_registered,
                        "has_cancelled": has_cancelled,
                        "active_membership": self.request.user.user_membership.active,
                        "time": time,
                    },
                )
        return render(
            request,
            "event/event_detail.html",
            {
                "form": AddEventMemberForm(),
                "event": event,
                "is_registered": is_registered,
                "has_cancelled": has_cancelled,
                "time": time,
            },
        )


class RegisterForEvent(View):
    def post(self, request):

        event_id = request.POST.get("event", None)
        user_id = request.POST.get("user", None)

        event = Event.objects.get(pk=event_id)
        user = User.objects.get(pk=user_id)

        if user.user_membership.membership.membership_type == "TRIAL":
            user_membership = UserMembership.objects.get(user=user)
            user_membership.remaining_trial_courses -= 1
            user_membership.save()

        inscription = EventMember(event=event, user=user)
        inscription.save()

        event.reserved_slot += 1
        event.save()
        messages.success(
            self.request, "Votre inscription au cours a bien été prise en compte.",
        )

        return redirect("event:event_calendar")


class UnsubscribeFromEvent(View):
    def post(self, request):

        event_id = request.POST.get("event", None)
        user_id = request.POST.get("user", None)

        event = Event.objects.get(pk=event_id)
        user = User.objects.get(pk=user_id)

        user_membership = UserMembership.objects.get(user=user)
        user_membership.remaining_trial_courses += 1
        user_membership.save()

        inscription = EventMember.objects.get(event=event, user=user)
        inscription.date_cancellation = datetime.now()
        inscription.save()

        event.reserved_slot -= 1
        event.save()

        messages.success(
            self.request, "Votre désinscription du cours a bien été prise en compte.",
        )

        return redirect("event:event_calendar")


class UserEventRegistrations(View):
    def get(self, request):
        user_registrations = Event.objects.filter(
            eventmember__user_id=request.user.pk,
            start__gte=timezone.now(),
            eventmember__date_cancellation__isnull=True,
        )

        registrations_list = []
        for event in user_registrations:
            registrations_list.append(event)

        return render(
            request,
            "event/user_events_registration.html",
            {"registrations_list": registrations_list},
        )

