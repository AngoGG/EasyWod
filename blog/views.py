from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from user.models import User

from .forms import ArticleForm, EditForm
from .models import Article

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
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    model = Article
    template_name = "blog/add_article.html"
    form_class = ArticleForm

    def post(self, request):
        error: bool = False

        form: ArticleForm = ArticleForm(request.POST)

        if form.is_valid():
            title: str = request.POST.get('title')
            author: User = User.objects.get(pk=request.POST.get('author'))
            body: str = request.POST.get('body')

            article: Article = Article.objects.create(
                title=title, author=author, body=body,
            )
            if article:
                return redirect('blog:article_list')
            else:
                error: bool = True
        return render(request, "blog/add_article.html", locals())


class UpdateArticleView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    model = Article
    template_name = "blog/update_article.html"
    form_class = EditForm


class DeleteArticleView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    model = Article
    template_name = "blog/delete_article.html"
    success_url = reverse_lazy("blog:article_list")

