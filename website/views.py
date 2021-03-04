from django.contrib import messages  # import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView, View

import config.settings as Settings
from .models import ContactMessage
from user.models import User

# Create your views here.


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "website/home.html")


class PasswordResetView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        reset_password_form: PasswordResetForm = PasswordResetForm()
        return render(
            request=request,
            template_name="website/reset_password.html",
            context={"reset_password_form": reset_password_form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        reset_password_form: PasswordResetForm = PasswordResetForm(self.request.POST)
        if reset_password_form.is_valid():
            data: str = reset_password_form.cleaned_data["email"]
            associated_users: QuerySet = User.objects.filter(Q(email=data))
            for user in associated_users:
                subject: str = "Réinitialisation du mot de passe demandée"
                email_template_name: str = "website/reset_password_email.txt"
                c: dict = {
                    "email": user.email,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "Pur Beurre",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email: str = render_to_string(email_template_name, c)
                try:
                    send_mail(
                        subject,
                        email,
                        Settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse("Paramètres invalides.")
            messages.success(
                request,
                "Un message contenant des instructions pour réinitialiser le mot de passe a été envoyé dans votre boîte de réception.",
            )
            return redirect("/")


class ContactView(View):
    def post(self, request):
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(
            request,
            "Votre demande a bien été envoyée, nous la traiterons dans les meilleurs délais",
        )
        return redirect("/")
