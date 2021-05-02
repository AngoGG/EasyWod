from django import forms


class NewsletterSubscribeForm(forms.Form):
    email = forms.CharField(label="Adresse email", max_length=255)
