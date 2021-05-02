from django.core import mail
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase

import config.settings as Settings
from user.models import User
from membership.models import Membership, UserMembership

import os
from io import BytesIO
from PIL import Image
from pathlib import Path


class TestRegistrationView(TestCase):
    def test_register_post(self) -> None:
        """Test if the url returns a correct 302 http status code
        and test if a user is correctly created.
        A new user must have an active TRIAL subscription.
        A new user must have the MEMBER type.
        """

        Membership.objects.create(membership_type="TRIAL")

        client: Client = Client()
        Settings.RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
        repatcha_test_public_key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
        response: HttpResponse = client.post(
            "/user/register",
            {
                "email": "matt-fraser@gmail.com",
                "first_name": "Matt",
                "last_name": "Fraser",
                "date_of_birth_year": 1997,
                "date_of_birth_month": 10,
                "date_of_birth_day": 4,
                "password1": "password8chars",
                "password2": "password8chars",
                'g-recaptcha-response': [repatcha_test_public_key],
                "submit": "Register",
            },
        )
        assert response.status_code == 302  # Testing redirection
        user_created: QuerySet = User.objects.first()  # type: ignore
        self.assertEqual("matt-fraser@gmail.com", user_created.email)
        self.assertTrue(user_created.check_password("password8chars"))
        self.assertEqual("Matt", user_created.first_name)
        self.assertEqual("Fraser", user_created.last_name)
        self.assertEqual("MEMBER", user_created.type)

        # Check if the User has a correct TRIAL membership
        self.assertEqual(
            "TRIAL", user_created.user_membership.membership.membership_type
        )

        # Check if the User subscription is active
        assert UserMembership.objects.filter(user=user_created, active=True).exists()

        # Check if mail if sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f"Activation de votre compte EasyWod.")

    def test_register_post_no_captcha(self):
        client: Client = Client(HTTP_HOST="localhost")
        Settings.RECAPTCHA_PRIVATE_KEY = str(os.environ.get("RECAPTCHA_PRIVATE_KEY"))
        response: HttpResponse = client.post(
            "/user/register",
            {
                "email": "matt-fraser@gmail.com",
                "first_name": "Matt",
                "last_name": "Fraser",
                "date_of_birth_year": 1997,
                "date_of_birth_month": 10,
                "date_of_birth_day": 4,
                "password1": "password8chars",
                "password2": "password8chars",
                'g-recaptcha-response': [''],
                "submit": "Register",
            },
        )

        message = User.objects.first()

        assert response.status_code == 200  # Testing redirection
        assert message is None

    def test_register_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        response: HttpResponse = client.get("/user/register")
        assert response.status_code == 200  # Testing redirection


class TestLoginView(TestCase):
    def test_login_success(self) -> None:
        """Test if the url returns a correct 302 http status code 
        when a user success to connect.
        """
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

        client: Client = Client()
        response: HttpResponse = client.post(
            "/user/login",
            {"email": ["matt-fraser@gmail.com"], "password": ["password8chars"],},
        )
        assert response.status_code == 302  # Testing redirection

    def test_login_fail(self) -> None:
        """When a login fails, there is no redirection 
        so it should returns a 200 http status code. 
        """
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        client: Client = Client()
        response: HttpResponse = client.post(
            "/user/login",
            {"email": ["matt-fraser@gmail.com"], "password": ["wrongpassword"],},
        )
        assert response.status_code == 200  # Testing redirection

    def test_login_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        response: HttpResponse = client.get("/user/login")
        assert response.status_code == 200  # Testing redirection


class TestLogoutView(TestCase):
    def test_logout(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        client: Client = Client()
        client.post(
            "/user/login",
            {"username": ["matt-fraser@gmail.com"], "password": ["password8chars"],},
        )
        response: HttpResponse = client.get("/user/logout",)
        assert response.status_code == 302  # Testing redirection


class TestProfileView(TestCase):
    def test_profile_redirection_not_authentificated(self):
        client: Client = Client()
        response: HttpResponse = client.get("/user/profile",)
        assert response.status_code == 302  # Testing redirection


class TestUserPasswordChangeView(TestCase):
    def test_change_password_ok(self):
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

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response: HttpResponse = client.post(
            "/user/change_password",
            {
                "old_password": ["password8chars"],
                "new_password1": ["newpassword8chars"],
                "new_password2": ["newpassword8chars"],
                "change_password": [""],
            },
        )

        user: QuerySet = User.objects.first()
        self.assertTrue(user.check_password("newpassword8chars"))

    def test_change_password_ko(self):
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

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")
        response: HttpResponse = client.post(
            "/user/change_password",
            {
                "old_password": ["password8chars"],
                "new_password1": ["newpassword8chars"],
                "new_password2": ["wrongpass"],
                "change_password": [""],
            },
        )

        user: QuerySet = User.objects.first()
        self.assertFalse(user.check_password("newpassword8chars"))


class TestUserUpdateView(TestCase):
    def test_access_page(self):
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

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")
        user: QuerySet = User.objects.first()

        response: HttpResponse = client.get(f"/user/update/{user.pk}")
        assert response.status_code == 200  # Testing redirection
        self.assertTemplateUsed(response, "user/user_update.html")

    def test_trying_access_other_user_page(self):
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        User.objects.create_user(
            email="jocelaing@gmail.com",
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

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        user: QuerySet = User.objects.last()

        response: HttpResponse = client.get(f"/user/update/{user.pk}")
        assert response.status_code == 404  # Testing redirection

    def test_update_info(self):
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

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")
        user: QuerySet = User.objects.first()

        assert user.address_info is None
        response: HttpResponse = client.post(
            f"/user/update/{user.pk}",
            {
                "email": ["matt-fraser@gmail.com"],
                "first_name": ["Matt"],
                "last_name": ["Fraser"],
                "address_info": ["Updated Address"],
                "address_additional_info": [""],
                "city": [""],
                "zip_code": [""],
                "country": [""],
            },
        )

        new_user: QuerySet = User.objects.first()
        assert new_user.address_info == "Updated Address"
        assert response.status_code == 302  # Testing redirection


class TestChangeProfilePictureView(TestCase):
    def create_image(
        self, storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'
    ):
        """
        Generate a test image, returning the filename that it was saved as.

        If ``storage`` is ``None``, the BytesIO containing the image data
        will be passed instead.
        """
        data = BytesIO()
        Image.new(image_mode, size).save(data, image_format)
        data.seek(0)
        if not storage:
            return data
        image_file = ContentFile(data.read())
        return storage.save(filename, image_file)

    def test_change_profile_picture(self):
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

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        user: QuerySet = User.objects.last()

        # set up form data
        avatar = self.create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())

        response: HttpResponse = client.post(
            f"/user/change_profile_picture",
            {"user_id": [user.id], "file": [avatar_file],},
            format='multipart',
        )
        updated_user: QuerySet = User.objects.last()
        profile_picture_path = Path(
            str(Settings.BASE_DIR) + '/..' + str(updated_user.profile_picture.url)
        )

        assert response.status_code == 302  # Testing redirection
        assert updated_user.profile_picture.url == '/media/profile_pictures/front.png'
        os.remove(profile_picture_path)


class TestMemberListView(TestCase):
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
        response = client.get("/user/member_list")
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
        response = client.get("/user/member_list")
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

        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user = User.objects.first()

        User.objects.create_user(
            email="user@gmail.com",
            password="password8chars",
            first_name="User",
            last_name="Testsearch",
            date_of_birth="1997-4-10",
        )

        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response = client.post(
            '/user/member_list',
            {
                'search': ['User'],
                'membership_type': ['premium', 'trial'],
                'membership_status': ['active', 'inactive'],
            },
        )

        for result in response.context["object_list"]:
            assert result.email == "user@gmail.com"
        assert response.status_code == 200

    def test_search_with_premium_membership(self):
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

        response = client.post(
            '/user/member_list',
            {
                'search': ['User'],
                'membership_type': ['premium'],
                'membership_status': ['active', 'inactive'],
            },
        )

        self.assertFalse(response.context["object_list"])

        assert response.status_code == 200

    def test_search_with_premium_membership_active(self):
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

        searched_user = User.objects.create_user(
            email="user@gmail.com",
            password="password8chars",
            first_name="User",
            last_name="Testsearch",
            date_of_birth="1997-4-10",
        )

        Membership.objects.create(membership_type="PREMIUM")
        premium_membership = Membership.objects.get(membership_type='PREMIUM')

        # Creating a new UserMembership

        user_membership = UserMembership.objects.create(
            user=searched_user, membership=premium_membership
        )
        user_membership.save()

        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response = client.post(
            '/user/member_list',
            {
                'search': [''],
                'membership_type': ['premium'],
                'membership_status': ['active'],
            },
        )

        for result in response.context["object_list"]:
            assert result.email == "user@gmail.com"

        assert response.status_code == 200

    def test_search_with_premium_membership_inactive(self):
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

        searched_user = User.objects.create_user(
            email="user@gmail.com",
            password="password8chars",
            first_name="User",
            last_name="Testsearch",
            date_of_birth="1997-4-10",
        )

        Membership.objects.create(membership_type="PREMIUM")
        premium_membership = Membership.objects.get(membership_type='PREMIUM')

        # Creating a new UserMembership

        user_membership = UserMembership.objects.create(
            user=searched_user, membership=premium_membership, active=False
        )
        user_membership.save()

        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response = client.post(
            '/user/member_list',
            {
                'search': [''],
                'membership_type': ['premium'],
                'membership_status': ['active'],
            },
        )

        for result in response.context["object_list"]:
            assert result.email == "user@gmail.com"

        assert response.status_code == 200

    def test_search_with_trial_membership(self):
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

        searched_user = User.objects.create_user(
            email="user@gmail.com",
            password="password8chars",
            first_name="User",
            last_name="Testsearch",
            date_of_birth="1997-4-10",
        )

        Membership.objects.create(membership_type="TRIAL")
        free_membership = Membership.objects.get(membership_type='TRIAL')

        # Creating a new UserMembership

        user_membership = UserMembership.objects.create(
            user=searched_user, membership=free_membership
        )
        user_membership.save()

        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response = client.post(
            '/user/member_list',
            {
                'search': [''],
                'membership_type': ['trial'],
                'membership_status': ['active', 'inactive'],
            },
        )
        for result in response.context["object_list"]:
            assert result.email == "user@gmail.com"

        assert response.status_code == 200

    def test_search_with_trial_membership_active(self):
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

        searched_user = User.objects.create_user(
            email="user@gmail.com",
            password="password8chars",
            first_name="User",
            last_name="Testsearch",
            date_of_birth="1997-4-10",
        )

        Membership.objects.create(membership_type="TRIAL")
        free_membership = Membership.objects.get(membership_type='TRIAL')

        # Creating a new UserMembership

        user_membership = UserMembership.objects.create(
            user=searched_user, membership=free_membership
        )
        user_membership.save()

        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response = client.post(
            '/user/member_list',
            {
                'search': [''],
                'membership_type': ['trial'],
                'membership_status': ['active'],
            },
        )

        for result in response.context["object_list"]:
            assert result.email == "user@gmail.com"

        assert response.status_code == 200

    def test_search_with_trial_membership_inactive(self):
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

        searched_user = User.objects.create_user(
            email="user@gmail.com",
            password="password8chars",
            first_name="User",
            last_name="Testsearch",
            date_of_birth="1997-4-10",
        )

        Membership.objects.create(membership_type="TRIAL")
        free_membership = Membership.objects.get(membership_type='TRIAL')

        # Creating a new UserMembership

        user_membership = UserMembership.objects.create(
            user=searched_user, membership=free_membership, active=False
        )
        user_membership.save()

        users = User.objects.filter(email="user@gmail.com")

        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response = client.post(
            '/user/member_list',
            {
                'search': [''],
                'membership_type': ['trial'],
                'membership_status': ['inactive'],
            },
        )

        for result in response.context["object_list"]:
            assert result.email == "user@gmail.com"

        assert response.status_code == 200
