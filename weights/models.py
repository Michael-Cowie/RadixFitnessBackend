from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Weights(models.Model):
    class Meta:
        unique_together = ('date', 'user_id')  # Do not allow multiple weight entries for the same day.

    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])
    notes = models.CharField(max_length=255, default='')

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'On {self.date}, you weighed {self.weight_kg}kg'
