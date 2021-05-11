from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from user.models import User

# Create your models here.


class Article(models.Model):
    title = models.CharField(_("Titre"), max_length=255)
    author = models.ForeignKey(User, verbose_name=_("Auteur"), on_delete=models.CASCADE)
    body = RichTextField(_("Contenu"))
    publication_date = models.DateTimeField(
        verbose_name=_("Date de publication"), auto_now_add=True
    )

    def __str__(self):
        return self.title + " | " + str(self.author)

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"pk": self.id})

