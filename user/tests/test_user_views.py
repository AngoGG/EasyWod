from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from user.models import User


class TestRegistrationView(TestCase):
    def test_register_post(self) -> None:
        """Test if the url returns a correct 302 http status code
        and test if a user is correctly created.
        """
        client: Client = Client()
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
                "submit": "Register",
            },
        )
        assert response.status_code == 302  # Testing redirection
        user_created: QuerySet = User.objects.first()  # type: ignore
        self.assertEqual("matt-fraser@gmail.com", user_created.email)
        self.assertTrue(user_created.check_password("password8chars"))
        self.assertEqual("Matt", user_created.first_name)
        self.assertEqual("Fraser", user_created.last_name)

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

