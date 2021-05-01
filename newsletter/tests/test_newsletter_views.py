from django.db.models.query import QuerySet
from django.test import Client, TestCase
from newsletter.models import SubscribedUsers


class TestSubscribeView(TestCase):
    def test_subscribe(self):
        # Sub
        client: Client = Client(HTTP_HOST="localhost")
        client.post(
            "/newsletter/", {"email": ["matt-fraser@gmail.com"]},
        )
        # Check mail
        subscribers = SubscribedUsers.objects.first()
        assert subscribers.email == "matt-fraser@gmail.com"

