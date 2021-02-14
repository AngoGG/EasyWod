from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "author", "body")

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Titre de l'article"}),
            "author": forms.TextInput(attrs={"value": "", "type": "hidden"}),
            "body": forms.TextInput(
                attrs={"placeholder": "Entrez le contenu de votre Article"}
            ),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "body")

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Titre de l'article"}),
            "body": forms.TextInput(
                attrs={"placeholder": "Entrez le contenu de votre Article"}
            ),
        }
