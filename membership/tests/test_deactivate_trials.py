from django.core import mail
from django.db.models.query import QuerySet
from django.test import TestCase
from django.core.management import call_command
from user.models import User
from blog.models import Article
from membership.libs import membership_queries
from membership.models import Membership, UserMembership


class TestDeactivateTrials(TestCase):
    def test_deactivate_trials(self):

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

        user_2 = User.objects.create_user(
            email="haley-adams@gmail.com",
            password="password8chars",
            first_name="Haley",
            last_name="Adams",
            date_of_birth="1997-4-10",
        )

        # Creating a new UserMembership
        user_membership_1 = UserMembership.objects.create(
            user=user, membership=trial_membership, remaining_trial_courses=0
        )
        user_membership_1.save()

        user_membership_2 = UserMembership.objects.create(
            user=user_2, membership=trial_membership, remaining_trial_courses=3
        )
        user_membership_2.save()

        call_command('deactivate_trials')

        inactive_user_memberships = UserMembership.objects.filter(active=False)

        assert user_membership_1 in inactive_user_memberships
        assert user_membership_2 not in inactive_user_memberships
