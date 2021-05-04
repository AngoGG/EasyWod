from django.test import TestCase

from user.models import User
from membership.models import Membership, UserMembership
from membership.libs import membership_queries


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
        premium_membership = Membership.objects.get(membership_type='TRIAL')

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
            user=user, membership=premium_membership, remaining_trial_courses=0
        )
        user_membership.save()

        trials_to_deactivate = membership_queries.get_trial_to_deactivate()
        assert "matt-fraser@gmail.com" in trials_to_deactivate
        assert "haley-adams@gmail.com" not in trials_to_deactivate

    def test_get_ending_trial_membership(self) -> None:
        pass
