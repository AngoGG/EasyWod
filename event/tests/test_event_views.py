from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from event.models import Event


class TestCalendarView(TestCase):
    def test_page_return_expected_html(self) -> None:
        client: Client = Client()
        response: HttpResponse = client.get("/event/")
        self.assertTemplateUsed(response, "event/event_calendar.html")
