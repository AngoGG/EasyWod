from datetime import datetime
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from event.models import Event


class TestCalendarView(TestCase):
    def test_page_return_expected_html(self) -> None:
        client: Client = Client()
        response: HttpResponse = client.get("/event/")
        self.assertTemplateUsed(response, "event/event_calendar.html")


class TestEventView(TestCase):
    def test_event_without_registration_access(self) -> None:
        name = "WOD"
        slot = "1"
        start = datetime.now()
        end = datetime.now()

        event = Event.objects.create(name=name, start=start, end=end, slot=slot)
        event.save()

        event_created: QuerySet = Event.objects.first()
        client: Client = Client()
        response: HttpResponse = client.get(f"/event/{event_created.pk}",)

        assert response.status_code == 200  # Testing redirection
