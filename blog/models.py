from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.


class Article(models.Model):
    title = models.CharField(_("Titre"), max_length=255)
    author = models.ForeignKey(User, verbose_name=_("Auteur"), on_delete=models.CASCADE)
    body = models.TextField(_("Contenu"))

    def __str__(self):
        return self.title + " | " + str(self.author)

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"pk": self.id})

