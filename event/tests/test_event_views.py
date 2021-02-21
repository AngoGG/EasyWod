from datetime import datetime
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from event.models import Event, EventMember
from user.models import User


class TestCalendarView(TestCase):
    def test_page_return_expected_html(self) -> None:
        client: Client = Client()
        response: HttpResponse = client.get("/event/")
        self.assertTemplateUsed(response, "event/event_calendar.html")


class TestEventView(TestCase):
    def test_event_without_registration_access(self) -> None:
        Event.objects.create(
            name="WOD", start=datetime.now(), end=datetime.now(), slot="1"
        )

        event_created: QuerySet = Event.objects.first()
        client: Client = Client()
        response: HttpResponse = client.get(f"/event/{event_created.pk}",)

        assert response.status_code == 200  # Testing redirection

    def test_event_with_registration_access(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        user_created: QuerySet = User.objects.first()  # type: ignore

        Event.objects.create(
            name="WOD", start=datetime.now(), end=datetime.now(), slot="1"
        )

        event_created: QuerySet = Event.objects.first()

        EventMember.objects.create(event=event_created, user=user_created)

        client: Client = Client()
        response: HttpResponse = client.get(f"/event/{event_created.pk}",)

        assert response.status_code == 200  # Testing redirection
