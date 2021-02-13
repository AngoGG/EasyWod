from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article

# Create your views here.


class BlogView(ListView):
    model = Article
    template_name = "blog/blog_home.html"


class ArticleView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
