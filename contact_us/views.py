from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages  # import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, ListView, View
from django.shortcuts import redirect

import requests

from .models import ContactMessage
import config.settings as Settings

from membership.models import Membership, UserMembership
from membership.libs import membership_queries
from newsletter.forms import NewsletterSubscribeForm
from user.models import User
from event.libs import event_queries


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
            return redirect('/')
        else:
            messages.error(
                request, "Captcha invalide, Veuillez réessayer.",
            )
            coaches = User.objects.filter(type="EMPLOYEE").count()
            customers = User.objects.filter(type="CUSTOMER").count()
            all_week_events = event_queries.get_all_week_events()
            newsletter_form: NewsletterSubscribeForm = NewsletterSubscribeForm()
            return render(
                request,
                "website/home.html",
                {
                    "coaches": coaches,
                    "customers": customers,
                    "all_week_events": all_week_events,
                    "newsletter_form": newsletter_form,
                    "contact_name": request.POST.get('name'),
                    "contact_email": request.POST.get('email'),
                    "contact_subject": request.POST.get('subject'),
                    "contact_message": request.POST.get('message'),
                },
            )


class ContactMessageView(DetailView):
    model = ContactMessage
    template_name = "contact_us/message_detail.html"


class AnswerContactMessageView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        subject: str = f"[{self.request.POST['subject']}] Réponse à votre demande"
        email: str = self.request.POST['message']
        contact_email: str = self.request.POST['contact_email']
        try:
            send_mail(
                subject,
                email,
                Settings.DEFAULT_FROM_EMAIL,
                [contact_email],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Paramètres invalides.")
        messages.success(
            request, "La réponse au message a bien été envoyé au demandeur.",
        )
        message = ContactMessage.objects.get(pk=self.request.POST['message_id'])
        message.answer = email
        message.answer_date = timezone.now()
        message.save()

        return redirect("/")


class ContactMessageListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    paginate_by = 10  # if pagination is desired
    template_name = "contact_us/contact_message_list.html"
    queryset = ContactMessage.objects.all()
    ordering = ['-message_date']

    def post(self, request):
        contact_message_status = request.POST.getlist('contact_message_status')
        if len(contact_message_status) == 1:
            if contact_message_status[0] == 'answered':
                result = ContactMessage.objects.filter(answer_date__isnull=False)
            else:
                result = ContactMessage.objects.filter(answer_date__isnull=True)
        else:
            result = ContactMessage.objects.all()
        return render(
            request, "contact_us/contact_message_list.html", {"object_list": result}
        )
