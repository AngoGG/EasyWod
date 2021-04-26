from django.contrib import admin
from django.urls import path

from . import views

app_name: str = "contact_us"

urlpatterns = [
    path(r"", views.ContactView.as_view(), name="contact"),
    path(
        r"message/<int:pk>", views.ContactMessageView.as_view(), name="message_detail"
    ),
    path(
        r"answer_message/",
        views.AnswerContactMessageView.as_view(),
        name="answer_message",
    ),
    path(
        r"contact_message_list",
        views.ContactMessageListView.as_view(),
        name="contact_message_list",
    ),
]
