"""easy_wod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views  # import this
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"", include("website.urls"), name="website"),
    path(r"blog/", include("blog.urls"), name="blog"),
    path(r"contact/", include("contact_us.urls"), name="contact"),
    path(r"event/", include("event.urls"), name="event"),
    path(f'membership/', include("membership.urls"), name='membership'),
    path(r"user/", include("user.urls"), name="user"),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="website/reset_password_confirm.html",
        ),
        name="reset_password_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="website/reset_password_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
