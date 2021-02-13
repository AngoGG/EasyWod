from django.urls import include, path
from .views import AddArticleView, ArticleView, BlogView

app_name: str = "blog"

urlpatterns = [
    path(r"", BlogView.as_view(), name="blog_home"),
    path(r"article/<int:pk>", ArticleView.as_view(), name="article_detail"),
    path(r"add_article/", AddArticleView.as_view(), name="add_article"),
]
