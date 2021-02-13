from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "author", "body")

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Titre de l'article"}),
            "body": forms.TextInput(
                attrs={"placeholder": "Entrez le contenu de votre Article"}
            ),
        }
