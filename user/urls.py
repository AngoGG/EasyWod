"""easy_wod URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfî
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import include
from django.conf import settings
from . import views

app_name: str = "user"

urlpatterns = [
    path(r"register", views.RegistrationView.as_view(), name="register"),
    path(r"login", views.LoginView.as_view(), name="login"),
    path(r"logout", views.LogoutView.as_view(), name="logout"),
    path(r"profile", views.ProfileView.as_view(), name="profile"),
]
