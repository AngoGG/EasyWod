from django.urls import include, path
from .views import ArticleView, BlogView

app_name: str = "blog"

urlpatterns = [
    path(r"", BlogView.as_view(), name="blog_home"),
    path(r"article/<int:pk>", ArticleView.as_view(), name="article_detail"),
]
