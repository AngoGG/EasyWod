from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import date

YEARS = [x for x in range(1900, date.today().year + 1)]


class RegisterForm(UserCreationForm):
    email: forms.EmailField = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': f'form-control',
                'placeholder': 'Entrez votre adresse Email',
            },
        ),
    )
    first_name: forms.CharField = forms.CharField(
        label="Prénom",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': f'form-control', 'placeholder': 'Entrez votre Prénom',},
        ),
    )
    last_name: forms.CharField = forms.CharField(
        label="Nom",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': f'form-control', 'placeholder': 'Entrez votre Nom',},
        ),
    )
    date_of_birth = forms.DateField(
        label="Quelle est votre date de naissance?",
        widget=forms.SelectDateWidget(years=YEARS, attrs={'class': f'form-select'},),
    )
    password1 = forms.CharField(
        label="Entrez votre mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'class': f'form-control',
                'placeholder': 'Entrez votre mot de passe',
            },
        ),
    )
    password2 = forms.CharField(
        label="Entrez votre mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'class': f'form-control',
                'placeholder': 'Confirmez votre mot de passe',
            },
        ),
    )

    class Meta:
        model = User
        fields: tuple = (
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "password1",
            "password2",
            "profile_picture",
        )


class ConnectionForm(forms.Form):
    email = forms.CharField(label="Adresse email", max_length=255)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
