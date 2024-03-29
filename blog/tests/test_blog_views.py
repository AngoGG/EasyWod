from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase

from blog.models import Article
from user.models import User


class TestBlogView(TestCase):
    def test_page_return_expected_html(self) -> None:
        client: Client = Client()
        response: HttpResponse = client.get("/blog/")
        self.assertTemplateUsed(response, "blog/article_list.html")


class TestAddArticleView(TestCase):
    def test_article_creation(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can create an Article, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore
        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            "/blog/add_article/",
            {"title": ["title"], "author": [str(user_created.pk)], "body": ["body"],},
        )

        article_created: QuerySet = Article.objects.first()  # type: ignore

        assert article_created.title == "title"
        assert article_created.body == "body"
        assert article_created.author == user_created

        assert response.status_code == 302  # Testing redirection

    def test_article_creation_access_forbidden(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )
        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get("/blog/add_article/",)

        assert response.status_code == 403  # Testing redirection

    def test_article_creation_post_forbidden(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        user_created: QuerySet = User.objects.first()  # type: ignore

        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            "/blog/add_article/",
            {"title": ["title"], "author": [str(user_created.pk)], "body": ["body"],},
        )

        assert Article.objects.first() is None  # type: ignore

        assert response.status_code == 403  # Testing redirection


class TestArticleView(TestCase):
    def test_article_access(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can create an Article, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore

        Article.objects.create(
            title="title", author=user_created, body="body",
        )
        article_created: QuerySet = Article.objects.first()  # type: ignore

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get(f"/blog/article/{article_created.pk}",)

        assert response.status_code == 200  # Testing redirection
        self.assertTemplateUsed(response, "blog/article_detail.html")

    def test_article_absent_redirection(self) -> None:
        client: Client = Client()

        response: HttpResponse = client.get(f"/blog/article/1",)

        assert response.status_code == 302  # Testing redirection


class TestUpdateArticleView(TestCase):
    def test_update_article(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can create an Article, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore
        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        Article.objects.create(
            title="title", author=user_created, body="body",
        )

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        article_created: QuerySet = Article.objects.first()  # type: ignore

        response: HttpResponse = client.post(
            f"/blog/update_article/{article_created.pk}",
            {"title": ["modified title"], "body": ["modified body"],},
        )

        article_created: QuerySet = Article.objects.first()  # type: ignore
        assert article_created.title == "modified title"
        assert article_created.body == "modified body"
        assert article_created.author == user_created

        assert response.status_code == 302  # Testing redirection

    def test_article_update_access_forbidden(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore
        Article.objects.create(
            title="title", author=user_created, body="body",
        )
        article_created: QuerySet = Article.objects.first()  # type: ignore
        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get(
            f"/blog/update_article/{article_created.pk}",
        )

        assert response.status_code == 403  # Testing redirection

    def test_article_update_post_forbidden(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore

        Article.objects.create(
            title="title", author=user_created, body="body",
        )
        article_created: QuerySet = Article.objects.first()  # type: ignore
        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            f"/blog/update_article/{article_created.pk}",
            {"title": ["modified title"], "body": ["modified body"],},
        )

        article_created: QuerySet = Article.objects.first()  # type: ignore

        assert article_created.title == "title"
        assert article_created.body == "body"

        assert response.status_code == 403  # Testing redirection


class TestDeleteArticleView(TestCase):
    def test_delete_article(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Only Employee can create an Article, so we need to set the correct user type
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.type = "EMPLOYEE"
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore

        Article.objects.create(
            title="title", author=user_created, body="body",
        )
        article_created: QuerySet = Article.objects.first()  # type: ignore
        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        article_created = Article.objects.first()

        response: HttpResponse = client.post(
            f"/blog/article/{article_created.pk}/delete", {},
        )

        assert Article.objects.first() is None  # type: ignore
        assert response.status_code == 302  # Testing redirection

    def test_article_delete_access_forbidden(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore
        Article.objects.create(
            title="title", author=user_created, body="body",
        )

        article_created: QuerySet = Article.objects.first()  # type: ignore

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.get(
            f"/blog/article/{article_created.pk}/delete",
        )

        assert response.status_code == 403  # Testing redirection

    def test_article_delete_post_forbidden(self) -> None:
        User.objects.create_user(
            email="matt-fraser@gmail.com",
            password="password8chars",
            first_name="Matt",
            last_name="Fraser",
            date_of_birth="1997-4-10",
        )

        # Account Activation
        users = User.objects.filter(email="matt-fraser@gmail.com")
        for user in users:
            user.is_active = True
            user.save()

        user_created: QuerySet = User.objects.first()  # type: ignore

        Article.objects.create(
            title="title", author=user_created, body="body",
        )

        client: Client = Client()
        client.login(username="matt-fraser@gmail.com", password="password8chars")

        response: HttpResponse = client.post(
            "/blog/article/1/delete", {},
        )

        assert Article.objects.first() is not None  # type: ignore

        assert response.status_code == 403  # Testing redirection

