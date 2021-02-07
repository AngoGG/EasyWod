import pytest
from django.db.models.query import QuerySet
from django.test import TestCase
from user.models import User
import datetime


class TestUserModel(TestCase):
    def test_create_user(self) -> None:
        """Test the correct user creation.
        """
        user: User = User.objects.create_user(
            email="mail@mail.com",
            password="password",
            first_name="firstname",
            last_name="lastname",
            date_of_birth=datetime.date(1997, 4, 10),
        )
        user_created: QuerySet = User.objects.first()
        self.assertEqual(user, user_created)
        self.assertEqual("mail@mail.com", user_created.email)
        self.assertTrue(user_created.check_password("password"))
        self.assertEqual("firstname", user_created.first_name)
        self.assertEqual("lastname", user_created.last_name)
        self.assertEqual(datetime.date(1997, 4, 10), user_created.date_of_birth)

    def test_create_superuser(self) -> None:
        """Test the correct user creation.
        """
        user: User = User.objects.create_superuser(
            email="mail@mail.com",
            password="password",
            first_name="firstname",
            last_name="lastname",
            date_of_birth=datetime.date(1997, 4, 10),
        )
        user_created: QuerySet = User.objects.first()
        self.assertEqual(user, user_created)
        self.assertEqual("mail@mail.com", user_created.email)
        self.assertTrue(user_created.check_password("password"))
        self.assertEqual("firstname", user_created.first_name)
        self.assertEqual("lastname", user_created.last_name)
        self.assertEqual(datetime.date(1997, 4, 10), user_created.date_of_birth)
        self.assertTrue(user_created.is_admin)
