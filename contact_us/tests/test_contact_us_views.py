from django.test import Client, TestCase
from user.models import User
from contact_us.models import ContactMessage
import config.settings as Settings

import os


class TestContactView(TestCase):
    def test_contact_view(self):
        client: Client = Client(HTTP_HOST="localhost")
        # Setting up Captcha setting keys
        Settings.RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
        repatcha_test_public_key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
        response = client.post(
            "/contact/",
            {
                'name': ['User'],
                'email': ['user@gmail.com'],
                'subject': ['Sujet important OK'],
                'message': ['Test'],
                'g-recaptcha-response': [repatcha_test_public_key],
            },
        )
        message = ContactMessage.objects.first()
        assert response.status_code == 302  # Testing redirection
        assert message.name == "User"
        assert message.email == "user@gmail.com"

    def test_contact_view_no_captcha(self):
        client: Client = Client(HTTP_HOST="localhost")
        Settings.RECAPTCHA_PRIVATE_KEY = str(os.environ.get("RECAPTCHA_PRIVATE_KEY"))
        response = client.post(
            "/contact/",
            {
                'name': ['User'],
                'email': ['user@gmail.com'],
                'subject': ['Sujet important KO'],
                'message': ['Test'],
                'g-recaptcha-response': [''],
            },
        )

        message = ContactMessage.objects.first()

        assert response.status_code == 302  # Testing redirection
        assert message is None
