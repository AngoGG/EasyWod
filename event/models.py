from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from user.models import User


class Event(models.Model):
    name = models.CharField(verbose_name=_("Nom de l'évènement"), max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    slot = models.IntegerField(verbose_name=_("Places disponibles"), default=10)

    def __str__(self):
        return self.name


class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(
        verbose_name=_("Date d'inscription"), auto_now_add=True
    )
    date_cancellation = models.DateTimeField(
        verbose_name=_("Date d'annulation"), null=True, blank=True
    )

    class Meta:
        unique_together = ["event", "user"]

    def __str__(self):
        return str(self.user)
