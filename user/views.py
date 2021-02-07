from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView
from .forms import RegisterForm
from .models import User
import datetime


# Create your views here.


class RegistrationView(FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "user/register.html", {"form": RegisterForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user registration.
        """

        email: str = request.POST.get("email")
        password: str = request.POST.get("password1")
        first_name: str = request.POST.get("first_name")
        last_name: str = request.POST.get("last_name")
        date_of_birth = f'{request.POST.get("date_of_birth_year")}-{request.POST.get("date_of_birth_month")}-{request.POST.get("date_of_birth_day")}'

        user: User = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        login(self.request, user)
        return redirect("/")
