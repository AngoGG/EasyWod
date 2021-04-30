from django.core import mail
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

        assert response.status_code == 200  # Testing redirection
        assert message is None


class TestContactMessageView(TestCase):
    def test_contact_message_access(self):
        # First we have to create a contact message
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

        print(f'HELLO MESSAGE : {message.id}')

        response = client.get(f"/contact/message/{message.id}")
        assert response.status_code == 200  # Testing redirection
        assert response.template_name == ["contact_us/message_detail.html"]


class TestAnswerContactMessageView(TestCase):
    def test_send_reset_email(self):
        # First we have to create a contact message
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

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        response = client.post(
            f"/contact/answer_message/",
            {
                "contact_email": [message.email],
                "subject": [message.subject],
                "message_id": [message.id],
                "message": "Voici une réponse à votre message",
            },
        )

        assert response.status_code == 302  # Testing redirection
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, f"[{message.subject}] Réponse à votre demande"
        )
