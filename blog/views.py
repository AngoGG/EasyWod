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


class AddArticleView(CreateView):
    model = Article
    template_name = "blog/add_article.html"
    form_class = ArticleForm


class UpdateArticleView(UpdateView):
    model = Article
    template_name = "blog/update_article.html"
    form_class = EditForm


class DeleteArticleView(DeleteView):
    model = Article
    template_name = "blog/delete_article.html"
    success_url = reverse_lazy("blog:article_list")

