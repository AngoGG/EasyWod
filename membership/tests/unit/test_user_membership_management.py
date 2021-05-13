from django.test import TestCase

from membership.libs import user_membership_management
from membership.models import Membership
from user.models import User


class TestUserMembershipManagement(TestCase):
    def test_create_user_trial_membership(self) -> None:
        """Test if we can access a user membership page
        """
        Membership.objects.create(membership_type="TRIAL")
        free_membership = Membership.objects.get(membership_type='TRIAL')

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        user = User.objects.first()

        # Creating a new UserMembership

        user_membership_management.create_user_trial_membership(user.id)

        user_with_membership = User.objects.first()

        self.assertEqual(True, user_with_membership.user_membership.active)
        self.assertEqual(
            free_membership.trial_courses,
            user_with_membership.user_membership.remaining_trial_courses,
        )
