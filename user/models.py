from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        MEMBER = "MEMBER", "Member"
        VISITOR = "VISITOR", "Visitor"

    type = models.CharField(max_length=50, choices=Types.choices, default=Types.MEMBER)
    email = models.EmailField(
        verbose_name=_("Adresse électronique"), max_length=255, unique=True,
    )
    date_of_birth = models.DateField(verbose_name=_("Date de Naissance"))
    first_name: models.EmailField = models.CharField(
        verbose_name=_("Prénom"), max_length=50, blank=True
    )
    last_name: models.EmailField = models.CharField(
        verbose_name=_("Nom"), max_length=50, blank=True,
    )
    address_info = models.CharField(
        verbose_name=_("Adresse"), max_length=255, null=True, blank=True
    )
    address_additional_info = models.CharField(
        _("Informations additionnelles adresse"), max_length=255, null=True, blank=True
    )
    city = models.CharField(_("Ville"), max_length=50, null=True, blank=True)
    zip_code = models.IntegerField(_("Code Postal"), null=True, blank=True)
    country = models.CharField(_("Pays"), max_length=50, null=True, blank=True)

    date_joined: models.EmailField = models.DateTimeField(
        verbose_name=_("Date d'inscription"), auto_now_add=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Customer(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
        return super().save(*args, **kwargs)


class Employee(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.EMPLOYEE
        return super().save(*args, **kwargs)


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.TYPE.CUSTOMER)


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.TYPE.EMPLOYEE)


class VisitorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.TYPE.VISITOR)

