from django.urls import path, include
from . import views

app_name = 'newsletter'

urlpatterns = [
    path(r"", views.SubscribeView.as_view(), name='subscribe'),
]

