from datetime import datetime, timedelta
from django.test import TestCase
from event.models import Event
from event.libs import event_queries


class TestEventQueries(TestCase):
    def test_get_all_week_events(self) -> None:
        event_1 = Event.objects.create(
            name="WOD", start=datetime.now(), end=datetime.now(), slot="1"
        )
        event_2 = Event.objects.create(
            name="WOD2", start=datetime.now(), end=datetime.now(), slot="1"
        )
        event_3 = Event.objects.create(
            name="WOD next week",
            start=datetime.now() - timedelta(days=7),
            end=datetime.now() - timedelta(days=8),
            slot="1",
        )
        all_week_events = event_queries.get_all_week_events()
        assert event_1 in all_week_events
        assert event_2 in all_week_events
        assert event_3 not in all_week_events
        assert all_week_events.count() == 2

    def test_get_weeks_events_average_attendees(self) -> None:
        Event.objects.create(
            name="WOD",
            start=datetime.now(),
            end=datetime.now(),
            slot="5",
            reserved_slot="1",
        )
        Event.objects.create(
            name="WOD2",
            start=datetime.now(),
            end=datetime.now(),
            slot="5",
            reserved_slot="5",
        )
        average_attendance = event_queries.get_weeks_events_average_attendees()

        assert average_attendance == 3

    def test_get_weeks_events_average_attendees_no_event(self) -> None:

        average_attendance = event_queries.get_weeks_events_average_attendees()

        assert average_attendance == 0
