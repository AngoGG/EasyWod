import requests
from django import forms
from django.contrib import messages  # import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, FormView, ListView, UpdateView, View

import config.settings as Settings
from membership.libs import membership_queries, user_membership_management

from .forms import ConnectionForm, RegisterForm, UpdatePasswordForm
from .models import User
from .tokens import account_activation_token


class RegistrationView(FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "user/register.html", {"form": RegisterForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user registration.
        """
        form = RegisterForm(request.POST)

        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = Settings.RECAPTCHA_PRIVATE_KEY

        data = {'secret': captcha_secret, 'response': captcha_token}
        captcha_server_response = requests.post(url=captcha_url, data=data)

        captcha_server_response = captcha_server_response.json()
        if captcha_server_response['success'] is True:
            if form.is_valid():
                email: str = form.cleaned_data["email"]
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
                user_created = User.objects.get(email=email)

                user_membership = user_membership_management.create_user_trial_membership(
                    user_created.id
                )

                current_site = get_current_site(request)
                mail_subject = 'Activation de votre compte EasyWod.'
                message = render_to_string(
                    'user/acc_active_email.html',
                    {
                        'user': user,
                        'domain': Settings.SITE_DOMAIN,
                        'protocol': 'https',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    },
                )
                email = EmailMessage(mail_subject, message, to=[email])
                email.send()

                messages.success(
                    request,
                    "Un email de confirmation vous a été envoyé, merci de consulter votre boite afin d'activer votre compte.",
                )
                return redirect("/")
            else:
                messages.error(
                    request, "Une erreur est survenue, veuillez réessayer.",
                )
                return render(request, "user/register.html", {"form": form})
        else:
            messages.error(
                request, "Captcha invalide, veuillez réessayer.",
            )
            return render(request, "user/register.html", {"form": form})

    def _clean_username(self, username):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Merci de votre confirmation. Vous pouvez maintenant vous connecter.",
            )
            return redirect("/")
        else:
            messages.error(
                request,
                "Le lien d'activation est invalide! Veuillez réessayer ou nous contacter.",
            )
            return redirect("/")


class LoginView(FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "user/connection.html", {"form": ConnectionForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user connection.
        """

        form: ConnectionForm = ConnectionForm(request.POST)

        if form.is_valid():
            username: str = form.cleaned_data["email"]
            password: str = form.cleaned_data["password"]
            user: User = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                messages.error(
                    request,
                    "L'utilisateur n'existe pas où le mot de passe est invalide, veuillez réessayer.",
                )
                return render(
                    request, "user/connection.html", {"form": form, "email": username}
                )
        return redirect("/")


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


class MemberDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

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
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
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
            {"form": UpdatePasswordForm(user=request.user)},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form: UpdatePasswordForm = UpdatePasswordForm(
            data=request.POST, user=request.user
        )

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                self.request, "Votre mot de passe a bien été modifié.",
            )
            return render(request, "user/profile.html")
        return render(request, "user/change_password.html", locals())


class MemberListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    paginate_by = 10  # if pagination is desired
    template_name = "user/member_list.html"
    queryset = User.objects.filter(type="MEMBER")
    ordering = ['-date_joined']

    def post(self, request):
        membership_type = request.POST.getlist('membership_type')
        membership_status = request.POST.getlist('membership_status')

        result = User.objects.filter(
            Q(first_name=request.POST['search']) | Q(last_name=request.POST['search'])
        )

        if not result.exists():
            if len(membership_type) == 2 or len(membership_type) == 0:
                if len(membership_status) == 1:
                    if membership_status[0] == 'active':
                        result = User.objects.filter(user_membership__active=True)
                    else:
                        result = User.objects.filter(user_membership__active=False)
                else:
                    result = User.objects.all()
            else:
                result = User.objects.filter(
                    user_membership__membership__membership_type=request.POST[
                        'membership_type'
                    ].upper()
                )
                if len(membership_status) == 1:
                    is_active: bool = membership_status[0] == 'active'
                    result = result.filter(user_membership__active=is_active)

        return render(request, 'user/member_list.html', {"object_list": result})


class ChangeProfilePictureView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user = User.objects.get(pk=request.POST['user_id'])
        user.profile_picture = request.FILES['file']
        if request.FILES['file'].content_type not in [
            'image/png',
            'image/jpeg',
            'image/jpg',
        ]:
            messages.error(
                self.request,
                "Votre photo de profile doit être au format png, jpeg ou jpg, veuillez rééssayer.",
            )
        elif request.FILES['file'].size > 2000000:
            messages.error(
                self.request,
                "Votre photo est trop lourde. Veuillez choisir une photo de moins de 2mo.",
            )
        else:
            print(f"FILE SIZE : {request.FILES['file'].size}")
            user.save()
            messages.success(
                self.request, "La photo de profil a bien été changée.",
            )
        return redirect('/user/profile')

