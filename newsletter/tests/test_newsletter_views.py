from django.db.models.query import QuerySet
from django.test import Client, TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from newsletter.models import SubscribedUsers


class TestSubscribeView(TestCase):
    def test_subscribe(self):
        # Sub
        client: Client = Client(HTTP_HOST="localhost")
        response = client.post("/newsletter/", {"email": ["matt-fraser@gmail.com"]},)
        # Check mail
        subscribers = SubscribedUsers.objects.first()
        assert subscribers.email == "matt-fraser@gmail.com"
        assert response.status_code == 302  # Testing redirection

