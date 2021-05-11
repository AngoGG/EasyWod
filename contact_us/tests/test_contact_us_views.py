import os

from django.core import mail
from django.test import Client, TestCase

import config.settings as Settings
from contact_us.models import ContactMessage
from user.models import User


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
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user = User.objects.first()

        client: Client = Client(HTTP_HOST="localhost")
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        ContactMessage.objects.create(
            name="User",
            email="user@gmail.com",
            subject="Sujet important OK",
            message="Test",
        )
        message = ContactMessage.objects.first()

        response = client.get(f"/contact/message/{message.id}")
        assert response.status_code == 200  # Testing redirection
        assert response.template_name == ["contact_us/message_detail.html"]

    def test_contact_message_access_forbidden(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        user = User.objects.first()

        client: Client = Client(HTTP_HOST="localhost")
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        ContactMessage.objects.create(
            name="User",
            email="user@gmail.com",
            subject="Sujet important OK",
            message="Test",
        )
        message = ContactMessage.objects.first()

        response = client.get(f"/contact/message/{message.id}")
        assert response.status_code == 403  # Testing redirection


class TestAnswerContactMessageView(TestCase):
    def test_send_answer_email(self):
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

        message = ContactMessage.objects.first()

        assert message.answer == "Voici une réponse à votre message"
        assert response.status_code == 302  # Testing redirection
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, f"[{message.subject}] Réponse à votre demande"
        )


class TestContactMessageListView(TestCase):
    def test_access_page(self):
        client: Client = Client(HTTP_HOST="localhost")
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user = User.objects.first()

        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response = client.get("/contact/messages_list")
        assert response.status_code == 200  # Testing redirection

    def test_access_page_not_employee(self):
        client: Client = Client(HTTP_HOST="localhost")
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()
        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response = client.get("/contact/messages_list")
        assert response.status_code == 403  # Testing redirection

    def test_search_by_name(self):
        client: Client = Client(HTTP_HOST="localhost")

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        ContactMessage.objects.create(
            name="User",
            email="user@mail.com",
            subject="Demande",
            message="Message Demande",
        )

        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user = User.objects.first()

        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response = client.post(
            '/contact/messages_list',
            {
                'search': ['monsieurx'],
                'contact_message_status': ['answered', 'to_answer'],
            },
        )
        for result in response.context["object_list"]:
            assert result.name == "User"
            self.assertIsNone(result.answer)
        assert response.status_code == 200

    def test_search_answered_message(self):
        client: Client = Client(HTTP_HOST="localhost")

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        ContactMessage.objects.create(
            name="User",
            email="user@mail.com",
            subject="Demande",
            message="Message Demande",
        )

        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user = User.objects.first()

        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response = client.post(
            '/contact/messages_list',
            {'search': [''], 'contact_message_status': ['answered'],},
        )

        for result in response.context["object_list"]:
            assert result.name == "User"
            self.assertIsNone(result.answer)
        self.assertFalse(response.context["object_list"])
        assert response.status_code == 200

    def test_search_to_answer_message(self):
        client: Client = Client(HTTP_HOST="localhost")

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        ContactMessage.objects.create(
            name="User",
            email="user@mail.com",
            subject="Demande",
            message="Message Demande",
        )

        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user = User.objects.first()

        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response = client.post(
            '/contact/messages_list',
            {'search': [''], 'contact_message_status': ['to_answer'],},
        )

        self.assertTrue(response.context["object_list"])

        for result in response.context["object_list"]:
            assert result.name == "User"
            self.assertIsNone(result.answer)

        assert response.status_code == 200
