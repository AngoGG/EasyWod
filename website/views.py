from os import environ

from django.contrib import messages  # import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
from event.libs import event_queries
from membership.models import Membership, UserMembership
from membership.libs import membership_queries
from user.models import User
from website.models import ContactMessage

import requests

# Create your views here.


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated and request.user.type == "EMPLOYEE":
            # Retrieving membership informations
            all_members = User.objects.filter(type="MEMBER")
            active_premium_members = (
                membership_queries.get_all_active_premium_membership()
            )
            inactive_premium_members = (
                membership_queries.get_all_inactive_premium_membership()
            )
            active_trial_members = membership_queries.get_all_active_trial_membership()
            inactive_trial_members = (
                membership_queries.get_all_inactive_trial_membership()
            )

            # Retrieving contact messages informations
            contact_messages = ContactMessage.objects.all()

            # Retrieving week events count
            all_week_events = event_queries.get_all_week_events()
            average_attendance = event_queries.get_weeks_events_average_attendees()

            return render(
                request,
                "website/home_employee.html",
                {
                    "members_info": {
                        "all_members": all_members,
                        "active_premium_members": active_premium_members,
                        "inactive_premium_members": inactive_premium_members,
                        "active_trial_members": active_trial_members,
                        "inactive_trial_members": inactive_trial_members,
                    },
                    "contact_messages": contact_messages,
                    "event_info": {
                        "all_week_events": all_week_events,
                        "average_attendance": average_attendance,
                    },
                },
            )
        else:
            coaches = User.objects.filter(type="EMPLOYEE").count()
            customers = User.objects.filter(type="CUSTOMER").count()
            all_week_events = event_queries.get_all_week_events()
            return render(
                request,
                "website/home.html",
                {
                    "coaches": coaches,
                    "customers": customers,
                    "all_week_events": all_week_events,
                },
            )


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

        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = Settings.RECAPTCHA_PRIVATE_KEY

        data = {'secret': captcha_secret, 'response': captcha_token}
        captcha_server_response = requests.post(url=captcha_url, data=data)

        captcha_server_response = captcha_server_response.json()

        if captcha_server_response['success'] is True:
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
        else:
            messages.error(
                request, "Captcha invalide, Veuillez réessayer.",
            )
        return redirect("/")
