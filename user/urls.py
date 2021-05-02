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

from django.conf.urls import include
from django.urls import path
from . import views

app_name: str = "user"

urlpatterns = [
    path(r"register", views.RegistrationView.as_view(), name="register"),
    path(
        r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ActivateView.as_view(),
        name='activate',
    ),
    path(r"login", views.LoginView.as_view(), name="login"),
    path(r"logout", views.LogoutView.as_view(), name="logout"),
    path(r"profile", views.ProfileView.as_view(), name="profile"),
    path(r"update/<int:pk>", views.ProfileUpdateView.as_view(), name="profile_update"),
    path(r"detail/<int:pk>", views.MemberDetailView.as_view(), name="detail"),
    path(
        r"detail/<int:pk>/update",
        views.MemberUpdateView.as_view(),
        name="member_update",
    ),
    path(r"member_list", views.MemberListView.as_view(), name="member_list"),
    path(
        "change_password",
        views.UserPasswordChangeView.as_view(),
        name="change_password",
    ),
    path(
        "change_profile_picture",
        views.ChangeProfilePictureView.as_view(),
        name="change_profile_picture",
    ),
]

