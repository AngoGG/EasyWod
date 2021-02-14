from django.core import mail
from django.test import Client, TestCase
from user.models import User


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
