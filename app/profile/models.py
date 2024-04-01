from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

alpha = RegexValidator(r'^[a-zA-Z]+$', 'Only alpha characters of length 1 or more are accepted')


class Units(models.TextChoices):
    METRIC = 'Metric', _('Metric')
    IMPERIAL = 'Imperial', _('Imperial')


class Profile(models.Model):
    name = models.TextField(validators=[alpha])
    measurement_system = models.CharField(choices=Units.choices, max_length=8)

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
