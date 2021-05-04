import json

from datetime import datetime
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from user.models import User
from membership.models import Membership, UserMembership


class TestMembershipView(TestCase):
    def test_access_page(self) -> None:
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

        # Only Employee can access the membership page, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.save()

        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(
            user=user, membership=free_membership
        )
        user_membership.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get(f"/membership/{user.pk}")
        self.assertTemplateUsed(response, "membership/list.html")

    def test_changing_membership(self) -> None:
        """Test if we can change a user membership
        """
        Membership.objects.create(membership_type="TRIAL")
        Membership.objects.create(membership_type="PREMIUM")
        free_membership = Membership.objects.get(membership_type='TRIAL')

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can access the membership page, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.save()

        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(
            user=user, membership=free_membership
        )
        user_membership.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        client.post(
            "/membership/", {'membership_type': ['PREMIUM'], 'member': [user.pk]}
        )

        user_modified: QuerySet = User.objects.first()  # type: ignore
        # Check if the User has a correct TRIAL membership
        self.assertEqual(
            "PREMIUM", user_modified.user_membership.membership.membership_type
        )
        self.assertIsNotNone(user_modified.user_membership.subscribtion_date)

    def test_deactivate_membership(self) -> None:
        """Test if we can deactivate a user membership
        """
        Membership.objects.create(membership_type="PREMIUM")
        premium_membership = Membership.objects.get(membership_type='PREMIUM')

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can access the membership page, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.save()

        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(
            user=user, membership=premium_membership
        )
        user_membership.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        client.post(
            f"/membership/deactivate", {'member': [user.pk]},
        )

        user_modified: QuerySet = User.objects.first()  # type: ignore
        # Check if the User has a correct TRIAL membership
        self.assertEqual(False, user_modified.user_membership.active)
        self.assertIsNotNone(user_modified.user_membership.unsubscription_date)

    def test_reactivate_membership(self) -> None:
        """Test if we can reactivate a user membership
        """
        Membership.objects.create(membership_type="PREMIUM")
        premium_membership = Membership.objects.get(membership_type='PREMIUM')

        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can access the membership page, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.save()

        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(
            user=user, membership=premium_membership, active=False
        )
        user_membership.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        client.post(
            f"/membership/reactivate", {'member': [user.pk]},
        )

        user_modified: QuerySet = User.objects.first()  # type: ignore
        # Check if the User has a correct TRIAL membership
        self.assertEqual(True, user_modified.user_membership.active)
        self.assertIsNotNone(user_modified.user_membership.unsubscription_date)


class TestUserMembershipView(TestCase):
    def test_create_user_membership(self) -> None:
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

        client: Client = Client()
        response: HttpResponse = client.get(f"/membership/create/{user.pk}")

        status: str = json.loads(response.content.decode('utf-8'))[
            'user_membership_status'
        ]

        user_with_membership = User.objects.first()

        self.assertEqual(True, user_with_membership.user_membership.active)
        self.assertEqual(
            free_membership.trial_courses,
            user_with_membership.user_membership.remaining_trial_courses,
        )
        self.assertEqual(status, 'created')
        assert response.status_code == 200
