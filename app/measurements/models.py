from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class WeightEntry(models.Model):
    class Meta:
        unique_together = (
            "date",
            "user_id",
        )  # Do not allow multiple weight entries for the same day.

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()
    """
    The original implementation of weight_kg was DecimalField(decimal_places=2, ...). Doing so, resulted in data loss
    when changing between units. The user is limited to a maximum of 2 decimal places, restricted by the UI, however
    if the user decides to use `lbs` as the unit and we store it with at most 2 decimal places in `kg`, it will
    result in data loss when converting it back. For example,
    
    kg_to_lbs = 2.2046226218488
    user_input = 165 (in lbs)
    
    This will result in ( user_input / kg_to_lbs ) = 74.84274104999918, being calculated, but we only stored 74.84
    
    Although, we can successfully convert this back while using this precise number, we cannot if we store
    it has 74.84. This is because 74.84 * kg_to_lbs = 164.9939570191642. To 2 decimal points of precision,
    this is 164.99, not 165. To resolve this, we create a "model" layer and a "view", where we never
    round any data inside the model and keep it intact, but perform the rounding when we want to display
    it to the user on the UI.
    """
    weight_kg = models.FloatField(validators=[MinValueValidator(1)])
    notes = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"On {self.date}, you weighed {self.weight_kg}kg"
