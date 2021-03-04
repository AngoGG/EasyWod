from django.contrib import admin
from django.urls import include, path

from . import views

app_name: str = "website"

urlpatterns = [
    path(r"", views.HomeView.as_view(), name="home"),
    path("reset_password/", views.PasswordResetView.as_view(), name="reset_password"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
