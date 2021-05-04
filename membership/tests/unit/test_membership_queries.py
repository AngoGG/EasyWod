from django.test import TestCase

from user.models import User
from membership.models import Membership, UserMembership
from membership.libs import membership_queries
from django.utils import timezone


class TestMembershipQueries(TestCase):
    def test_get_all_active_membership(self) -> None:

        # Create some membership
        # Run get_all_active_membership()
        # Check if the created membership email are in the reponse list

        Membership.objects.create(membership_type="PREMIUM")
        premium_membership = Membership.objects.get(membership_type='PREMIUM')

        user_1 = User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        # Creating a new UserMembership
        user_membership_1 = UserMembership.objects.create(
            user=user_1, membership=premium_membership
        )
        user_membership_1.save()

        user_2 = User.objects.create_user(
            email="haley-adams@gmail.com",
            password="password8chars",
            first_name="Haley",
            last_name="Adams",
            date_of_birth="1997-4-10",
        )
        # Creating a new UserMembership
        user_membership_2 = UserMembership.objects.create(
            user=user_2, membership=premium_membership
        )
        user_membership_2.save()

        active_membership_list = membership_queries.get_all_active_membership()
        assert "haley-adams@gmail.com" in active_membership_list
        assert "matt-fraser@gmail.com" in active_membership_list

    def test_get_trial_to_deactivate(self) -> None:
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
        user_membership = UserMembership.objects.create(
            user=user, membership=trial_membership, remaining_trial_courses=0
        )
        user_membership.save()

        user_membership_2 = UserMembership.objects.create(
            user=user_2, membership=trial_membership, remaining_trial_courses=3
        )
        user_membership_2.save()

        trials_to_deactivate = membership_queries.get_trial_to_deactivate()
        assert user_membership in trials_to_deactivate
        assert user_membership_2 not in trials_to_deactivate

    def test_get_ending_trial_membership(self) -> None:
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
        user_membership = UserMembership.objects.create(
            user=user,
            membership=trial_membership,
            active=False,
            unsusbcription_date=timezone.now() - timezone.timedelta(1),
        )
        user_membership.save()

        user_membership_2 = UserMembership.objects.create(
            user=user_2,
            membership=trial_membership,
            active=False,
            unsusbcription_date=timezone.now() - timezone.timedelta(6),
        )
        user_membership_2.save()

        previous_day_ended_trials = membership_queries.get_previous_day_ended_trial()

        assert user_membership.email in previous_day_ended_trials
        assert user_membership_2.email not in previous_day_ended_trials
