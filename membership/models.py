from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User

MEMBERSHIP_CHOICES = (('PREMIUM', 'Premium'), ('TRIAL', 'Trial'))


class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(
        verbose_name=_("Type d'abonnement"),
        choices=MEMBERSHIP_CHOICES,
        default='TRIAL',
        max_length=30,
    )
    price = models.DecimalField(
        verbose_name=_("Prix de l'abonnement"),
        default=0,
        max_digits=5,
        decimal_places=2,
    )
    trial_courses = models.IntegerField(
        verbose_name=_("Nombre de cours d'essai"), default=3, blank=True, null=True
    )

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user: User = models.OneToOneField(
        User, related_name='user_membership', on_delete=models.CASCADE
    )
    membership: Membership = models.ForeignKey(
        Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True
    )
    remaining_trial_courses = models.IntegerField(
        verbose_name=_("Nombre de cours d'essai restants"), blank=True, null=True,
    )
    active: models.BooleanField = models.BooleanField(default=True)
    subscribtion_date: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Date d'abonnement"), null=True
    )
    unsubscription_date: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Date de désabonnement"), null=True, blank=True
    )

    def __str__(self):
        return self.user.email
