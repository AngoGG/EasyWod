from django import forms
from .models import Article
from ckeditor.fields import RichTextField


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("body",)

        widgets = {
            "body": RichTextField(),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "body")

        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Titre de l'article", "class": "form-control"}
            ),
            "body": forms.TextInput(
                attrs={"placeholder": "Entrez le contenu de votre Article"}
            ),
        }
