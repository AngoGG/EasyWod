from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.


def blog_home(request):
    return render(request, "blog/blog_home.html", {})

