from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from membership.models import Membership, UserMembership
from user.models import User


class TestSendNewsletter(TestCase):
    def test_send_newsletter(self):

        Membership.objects.create(membership_type="TRIAL")
        trial_membership = Membership.objects.get(membership_type='TRIAL')

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        user = User.objects.get(email="matt-fraser@gmail.com")
        user.is_active = True
        user.save()

        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(
            user=user,
            membership=trial_membership,
            active=False,
            unsubscription_date=timezone.now() - timezone.timedelta(1),
        )
        user_membership.save()

        call_command('send_end_trial_alert')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, f"EasyWod - Fin de votre offre d'essai !"
        )
