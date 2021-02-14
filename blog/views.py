from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import Article
from .forms import ArticleForm, EditForm


# Create your views here.


class BlogView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    ordering = ["-publication_date"]


class ArticleView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"


class AddArticleView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    model = Article
    template_name = "blog/add_article.html"
    form_class = ArticleForm


class UpdateArticleView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    model = Article
    template_name = "blog/update_article.html"
    form_class = EditForm


class DeleteArticleView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    model = Article
    template_name = "blog/delete_article.html"
    success_url = reverse_lazy("blog:article_list")

