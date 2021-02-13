from django.urls import include, path
from . import views

app_name: str = "blog"

urlpatterns = [
    path(r"", views.blog_home, name="blog_home"),
]
