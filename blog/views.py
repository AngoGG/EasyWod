from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from .models import Article
from .forms import ArticleForm

# Create your views here.


class BlogView(ListView):
    model = Article
    template_name = "blog/blog_home.html"


class ArticleView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"


class AddArticleView(CreateView):
    model = Article
    template_name = "blog/add_article.html"
    form_class = ArticleForm
