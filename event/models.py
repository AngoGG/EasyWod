from django.db import models
from django.urls import reverse
from user.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
