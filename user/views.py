import datetime
from django.contrib import messages  # import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, FormView, ListView, View, UpdateView
from .forms import ConnectionForm, RegisterForm
from .models import User
from membership.libs import membership_queries
from membership.models import Membership, UserMembership


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

        free_membership = Membership.objects.get(membership_type='TRIAL')

        user: User = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )

        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(
            user=user, membership=free_membership
        )
        user_membership.save()

        # Creating a new UserSubscription
        user_subscription = Subscription()
        user_subscription.user_membership = user_membership
        user_subscription.save()

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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return render(request, "user/profile.html", **kwargs)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    model = User
    template_name = "user/user_update.html"
    fields = [
        'email',
        'first_name',
        'last_name',
        'address_info',
        'address_additional_info',
        'city',
        'zip_code',
        'country',
    ]

    def get_queryset(self):
        queryset = super(ProfileUpdateView, self).get_queryset()
        return queryset.filter(pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(
            self.request, "Vos informations ont bien été mises à jour.",
        )
        return reverse('user:profile')


class MemberDetailView(DetailView):
    model = User
    context_object_name = "member"
    template_name = "user/member_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_membership'] = membership_queries.get_all_active_membership()
        return context


class MemberUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    model = User
    context_object_name = "member"
    template_name = "user/user_update.html"
    fields = [
        'email',
        'first_name',
        'last_name',
        'address_info',
        'address_additional_info',
        'city',
        'zip_code',
        'country',
    ]

    def get_success_url(self):
        messages.success(
            self.request, "Les informations du membre ont bien été mises à jour.",
        )
        return reverse('user:member_list')


class UserPasswordChangeView(LoginRequiredMixin, FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "user/change_password.html",
            {"form": PasswordChangeForm(user=request.user)},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form: PasswordChangeForm = PasswordChangeForm(
            data=request.POST, user=request.user
        )

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, "user/profile.html")
        return render(request, "user/change_password.html", locals())


class MemberListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return (
            True
            if self.request.user.is_authenticated
            and self.request.user.type == "EMPLOYEE"
            else False
        )

    paginate_by = 10  # if pagination is desired
    template_name = "user/member_list.html"
    queryset = User.objects.filter(type="MEMBER")
    paginate_by = 10
    ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_membership'] = membership_queries.get_all_active_membership()
        return context
