from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DailyMacronutrientGoal(models.Model):
    class Meta:
        unique_together = (
            "date",
            "user_id",
        )  # Do not allow multiple tracking entries for the same day.

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    goal_calories = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_protein = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_carbs = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_fats = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    def __str__(self):
        return f"""
        On { self.date} you have have the following goals,

        - Goal calories { self.goal_calories }
        - Goal protein { self.goal_protein }
        - Goal carbs { self.goal_carbs }
        - Goal fats { self.goal_fats }
"""


class WeightGoal(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    goal_date = models.DateField()
    goal_weight_kg = models.FloatField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"I want to be {self.goal_weight_kg} by {self.goal_date}"
