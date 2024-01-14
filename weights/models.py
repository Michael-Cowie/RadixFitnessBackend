from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Units(models.TextChoices):
    KILOGRAM = 'kg', _('Kilogram')
    POUND = 'lbs', _('Pound')


class Weights(models.Model):
    class Meta:
        unique_together = ('date', 'user_id')  # Do not allow multiple weight entries for the same day.

    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])
    unit = models.CharField(choices=Units.choices, max_length=3)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'On {self.date}, you weighed {self.weight}{self.unit}'
