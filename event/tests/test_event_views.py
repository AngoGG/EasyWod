import json
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from django.utils import timezone
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
            name="WOD", start=timezone.now(), end=timezone.now(), slot="1"
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
            name="WOD", start=timezone.now(), end=timezone.now(), slot="1"
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
        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

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
            user.is_active = True
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
            user.is_active = True
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
                "period": ["2"],
                "frequency": ["daily"],
            },
        )

        event_created: QuerySet = Event.objects.first()

        assert event_created.name == "WOD"
        assert event_created.slot == 1

        assert response.status_code == 302  # Testing redirection

    def test_daily_event(self):
        # Test send Daily starting today with 7 days
        # Query Event should return 7 events with same hour

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
            user.is_active = True
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
                "period": ["1"],
                "frequency": ["daily"],
            },
        )
        assert Event.objects.count() == 7
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=20
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=21
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=22
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=23
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=24
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=25
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=26
        ).exists()

        Event.objects.all().delete()

        response: HttpResponse = client.post(
            "/event/add_event",
            {
                "name": ["WOD"],
                "date": ["2021-02-20"],
                "slot": ["1"],
                "start_time": ["15:00"],
                "end_time": ["16:00"],
                "period": ["2"],
                "frequency": ["daily"],
            },
        )
        assert Event.objects.count() == 14

        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=20
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=21
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=22
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=28
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=3, start__day=2
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=3, start__day=3
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=3, start__day=4
        ).exists()

        assert response.status_code == 302  # Testing redirection

    def test_weekly_event(self):
        # Test send Daily starting today with 7 days
        # Query Event should return 7 events with same hour

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
            user.is_active = True
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
                "period": ["1"],
                "frequency": ["weekly"],
            },
        )
        assert Event.objects.count() == 1

        Event.objects.all().delete()

        response: HttpResponse = client.post(
            "/event/add_event",
            {
                "name": ["WOD"],
                "date": ["2021-02-20"],
                "slot": ["1"],
                "start_time": ["15:00"],
                "end_time": ["16:00"],
                "period": ["5"],
                "frequency": ["weekly"],
            },
        )
        assert Event.objects.count() == 5

        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=20
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=2, start__day=27
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=3, start__day=3
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=3, start__day=10
        ).exists()
        assert Event.objects.filter(
            start__year=2021, start__month=3, start__day=17
        ).exists()

        assert response.status_code == 302  # Testing redirection


class TestRegisterForEvent(TestCase):
    def test_register(self):
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
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore

        Event.objects.create(
            name="WOD", start=timezone.now(), end=timezone.now(), slot="1"
        )

        event_created: QuerySet = Event.objects.first()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            "/event/register_event",
            {"user": user_created.pk, "event": event_created.pk,},
        )

        event = Event.objects.first()
        user = User.objects.first()

        assert event.eventmember_set.filter(user_id=user.pk).exists()
        assert response.status_code == 302  # Testing redirection


class TestUnsubscribeFromEvent(TestCase):
    def test_unsubscribe(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        user_created: QuerySet = User.objects.first()  # type: ignore

        Event.objects.create(
            name="WOD", start=timezone.now(), end=timezone.now(), slot="1"
        )

        event_created: QuerySet = Event.objects.first()

        EventMember.objects.create(event=event_created, user=user_created)

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            "/event/unsubscribe_event",
            {"user": user_created.pk, "event": event_created.pk,},
        )

        assert (
            event_created.eventmember_set.filter(user_id=user_created.pk).exists()
            is True
        )

        assert response.status_code == 302  # Testing redirection


class TestUserRegistrations(TestCase):
    def test_get_user_registrations(self):
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
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore

        Event.objects.create(
            name="WOD", start=timezone.now(), end=timezone.now(), slot="1"
        )

        event_created: QuerySet = Event.objects.first()

        EventMember.objects.create(event=event_created, user=user_created)

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get("/event/user_registrations",)

        self.assertEqual(
            json.loads(response.content),
            {"events": [{"name": "WOD", "id": event_created.pk}]},
        )

