from django.db import models
from django.urls import reverse
from user.models import User


class Event(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
