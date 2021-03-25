from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


@receiver(post_save, sender=User)
def save_password(sender, instance, created, **kwargs):
    if created:
        instance.set_password(instance.password)
        instance.save()


class University(models.Model):
    rank = models.IntegerField()
    name = models.CharField(max_length=256)
    course = models.CharField(max_length=256, null=True, blank=True)
    link_program_highlights = models.URLField()
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name} - {self.country}"


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    start_month = models.CharField(max_length=256, null=True, blank=True)
    avg_work_exp = models.IntegerField(null=True, blank=True)
    avg_student_age = models.IntegerField(null=True, blank=True)
    women_students = models.IntegerField(null=True, blank=True)
    avg_salary = models.IntegerField(null=True, blank=True)
    scholarship = models.BooleanField(default="No")
    accreditations = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.university.name}-{self.start_month}"
