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
        message.answer_date = timezone.now()
        message.save()

        print(f'LE MESSAGE : {message.answer_date}')
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
