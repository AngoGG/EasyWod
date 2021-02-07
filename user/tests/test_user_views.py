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
