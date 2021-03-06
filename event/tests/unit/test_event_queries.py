from datetime import datetime, timedelta
from django.test import TestCase
from event.models import Event
from event.libs import event_queries


class TestEventQueries(TestCase):
    def test_get_all_week_events(self) -> None:
        Event.objects.create(
            name="WOD", start=datetime.now(), end=datetime.now(), slot="1"
        )
        Event.objects.create(
            name="WOD2", start=datetime.now(), end=datetime.now(), slot="1"
        )
        Event.objects.create(
            name="WOD next week",
            start=datetime.now() - timedelta(days=7),
            end=datetime.now() - timedelta(days=8),
            slot="1",
        )
        all_week_events = event_queries.get_all_week_events()

        assert all_week_events == 2
