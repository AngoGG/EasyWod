from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, FormView, View


# Create your views here.
from django.urls import reverse_lazy

from .forms import NewsletterSubscribeForm
from .models import SubscribedUsers


class SubscribeView(CreateView):
    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user connection.
        """
        form: NewsletterSubscribeForm = NewsletterSubscribeForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data["email"]
            subscribe_user, created = SubscribedUsers.objects.get_or_create(email=email)
            subscribe_user.value = email
            subscribe_user.save()
            messages.success(
                self.request,
                "Votre inscription à la newsletter a bien été prise en compte.",
            )
        else:
            messages.error(
                self.request, "Une erreur est survenue, veuillez réessayer plus tard.",
            )
        return redirect('/')


class UnsubscribeView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, "newsletter/unsubscribe.html")

    def post(self, request, *args, **kwargs):
        user_id = urlsafe_base64_decode(kwargs['uidb64'])
        user = SubscribedUsers.objects.filter(pk=user_id)
        if user:
            user.delete()
        messages.success(
            self.request,
            "Votre désinscription à la newsletter a bien été prise en compte.",
        )
        return redirect('/')
