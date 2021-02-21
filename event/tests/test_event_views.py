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


class TestAddEvent(TestCase):
    def test_access_redirection_not_connected(self):
        client: Client = Client()
        response: HttpResponse = client.get("/event/add_event")
        assert response.status_code == 302  # Testing redirection

    def test_add_event_redirection_not_connected(self):
        client: Client = Client()
        response: HttpResponse = client.post("/event/add_event")
        assert response.status_code == 302  # Testing redirection

    def test_add_event_access_forbidden(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post("/event/add_event")
        assert response.status_code == 403  # Testing redirection

    def test_add_event_access(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can create an Event, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get("/event/add_event")
        assert response.status_code == 200  # Testing redirection

    def test_event_creation(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can create an Article, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            "/event/add_event",
            {
                "name": ["WOD"],
                "date": ["2021-02-20"],
                "slot": ["1"],
                "start_time": ["15:00"],
                "end_time": ["16:00"],
            },
        )

        event_created: QuerySet = Event.objects.first()

        assert event_created.name == "WOD"
        assert event_created.slot == 1

        assert response.status_code == 302  # Testing redirection
