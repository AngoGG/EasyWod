from django.core import mail
from django.test import Client, TestCase
from user.models import User
from website.models import ContactMessage


class TestPasswordResetView(TestCase):
    def test_send_reset_email(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        client: Client = Client(HTTP_HOST="localhost")
        response = client.post(
            "/reset_password/",
            {"email": ["matt-fraser@gmail.com"], "change_password": [""],},
        )

        assert response.status_code == 302  # Testing redirection
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Réinitialisation du mot de passe demandée"
        )


class TestContactView(TestCase):
    def test_contact_view(self):
        client: Client = Client(HTTP_HOST="localhost")
        response = client.post(
            "/contact/",
            {
                'name': ['User'],
                'email': ['user@gmail.com'],
                'subject': ['Sujet important'],
                'message': ['Test'],
            },
        )
        message = ContactMessage.objects.first()
        assert response.status_code == 302  # Testing redirection
        assert message.name == "User"
        assert message.email == "user@gmail.com"
