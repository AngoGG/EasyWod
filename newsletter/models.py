from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


# Create your models here.


class SubscribedUsers(models.Model):
    email: models.EmailField = models.EmailField(
        verbose_name=_("Adresse électronique"), max_length=255, unique=True,
    )

    def __str__(self):
        return self.name
