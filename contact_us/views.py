from django.shortcuts import render

# Create your views here.
from django.contrib import messages  # import messages
from django.views.generic import View
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
