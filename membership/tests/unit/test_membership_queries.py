from django.test import TestCase
from user.models import User
from membership.models import Membership, UserMembership, Subscription
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
        # Creating a new UserSubscription
        user_subscription_1 = Subscription()
        user_subscription_1.user_membership = user_membership_1
        user_subscription_1.save()

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
        # Creating a new UserSubscription
        user_subscription_2 = Subscription()
        user_subscription_2.user_membership = user_membership_2
        user_subscription_2.save()

        active_membership_list = membership_queries.get_all_active_membership()
        assert "haley-adams@gmail.com" in active_membership_list
        assert "matt-fraser@gmail.com" in active_membership_list
