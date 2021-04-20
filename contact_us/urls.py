from django.contrib import admin
from django.urls import path

from . import views

app_name: str = "contact_us"

urlpatterns = [
    path(r"", views.ContactView.as_view(), name="contact"),
    path(
        r"message/<int:pk>", views.ContactMessageView.as_view(), name="message_detail"
    ),
]
