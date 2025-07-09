from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

alpha = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Only alphabetic characters are allowed.",
)


class Units(models.TextChoices):
    METRIC = "Metric", _("Metric")
    IMPERIAL = "Imperial", _("Imperial")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    name = models.CharField(max_length=100, validators=[alpha])
    measurement_system = models.CharField(choices=Units.choices, max_length=8)

    def __str__(self):
        return self.name
