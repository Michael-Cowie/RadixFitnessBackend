from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

MACRO_NUTRIENTS = ["calories", "protein", "carbs", "fats"]
CURRENT_COLUMNS = [f"current_{macro_nutrient}" for macro_nutrient in MACRO_NUTRIENTS]
GOAL_COLUMNS = [f"goal_{macro_nutrient}" for macro_nutrient in MACRO_NUTRIENTS]


class DailyIntakeTracking(models.Model):
    class Meta:
        unique_together = (
            "date",
            "user_id",
        )  # Do not allow multiple tracking entries for the same day.

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    current_calories = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_calories = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    current_protein = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_protein = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    current_carbs = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_carbs = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    current_fats = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    goal_fats = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    def __str__(self):
        return f"""
        On { self.date} you have have the following intake,

        - Calories { self.current_calories } / { self.goal_calories }
        - Protein { self.current_protein} / { self.goal_protein }
        - Carbs { self.current_carbs } / { self.goal_carbs }
        - Fats { self.current_fats } / { self.goal_fats }
"""
