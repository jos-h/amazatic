from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


def length_validator(value):
    if not str(value).__len__() == 10:
        raise ValidationError(
            _('%(value)s must be of 10 digits'),
            params={'value': value},
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    full_name = models.TextField()
    phone = models.IntegerField(validators=[length_validator])

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email


class University(models.Model):
    rank = models.IntegerField()
    name = models.CharField(max_length=256)
    course = models.CharField(max_length=256)
    link_program_highlights = models.URLField()
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name} - {self.country}"


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    start_month = models.CharField(max_length=256)
    avg_work_exp = models.IntegerField()
    avg_student_age = models.IntegerField()
    women_students = models.IntegerField()
    avg_salary = models.IntegerField()
    scholarship = models.BooleanField(default="No")
    accreditations = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.university.name}-{self.start_month}"
