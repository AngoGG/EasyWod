from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True,
    )
    date_of_birth = models.DateField()
    first_name: models.EmailField = models.CharField(
        "first name", max_length=50, blank=True
    )
    last_name: models.EmailField = models.CharField(
        "last name", max_length=50, blank=True
    )
    date_joined: models.EmailField = models.DateTimeField(
        "date joined", auto_now_add=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

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
