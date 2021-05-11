from django.core import mail
from django.core.management import call_command
from django.db.models.query import QuerySet
from django.test import TestCase

from blog.models import Article
from newsletter.models import SubscribedUsers
from user.models import User


class TestSendNewsletter(TestCase):
    def test_send_newsletter(self):

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        user_created: QuerySet = User.objects.first()
        # Créer article
        Article.objects.create(
            title="title", author=user_created, body="body",
        )

        SubscribedUsers.objects.create(email="question@gmail.com")

        call_command('send_newsletter')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, f"EasyWod - Les articles de la semaine!"
        )
