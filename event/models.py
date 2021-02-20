from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from user.models import User


class Event(models.Model):
    name = models.CharField(verbose_name=_("Nom de l'évènement"), max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
