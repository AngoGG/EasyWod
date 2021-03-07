from django.urls import path, include
from . import views

app_name = 'membership'

urlpatterns = [
    path('', views.MembershipView.as_view(), name='select'),
]
