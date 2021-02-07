import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, View
from .forms import ConnectionForm, RegisterForm
from .models import User


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


class LoginView(FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "user/connection.html", {"form": ConnectionForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user connection.
        """
        error: bool = False

        form: ConnectionForm = ConnectionForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["email"]
            password: str = form.cleaned_data["password"]
            user: User = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                error: bool = True
        return render(request, "user/connection.html", locals())


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect("/")
