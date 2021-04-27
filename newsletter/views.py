from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView


# Create your views here.
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
