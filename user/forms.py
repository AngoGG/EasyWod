from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import date

YEARS = [x for x in range(1900, date.today().year + 1)]


class RegisterForm(UserCreationForm):
    email: forms.EmailField = forms.EmailField(
        max_length=255,
        required=True,
        help_text="Obligatoire. Renseignez une addresse mail valide.",
    )
    first_name: forms.CharField = forms.CharField(label="Prénom", max_length=50)
    last_name: forms.CharField = forms.CharField(label="Nom", max_length=50)
    date_of_birth = forms.DateField(
        label="What is your birth date?", widget=forms.SelectDateWidget(years=YEARS)
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
        )
