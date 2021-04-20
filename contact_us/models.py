from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    name = models.CharField(_("Nom"), max_length=50)
    email = models.EmailField(_("Adresse Mail"), max_length=254)
    subject = models.CharField(_("Sujet"), max_length=50)
    message = models.CharField(_("Message"), max_length=50)
    message_date = models.DateField(_("Date du message"), auto_now_add=True)
    answer_date = models.DateField(_("Date de réponse"), null=True)

    def __str__(self):
        return self.subject

