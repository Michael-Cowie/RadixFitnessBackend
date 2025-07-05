from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

MACRO_NUTRIENTS = ["calories", "protein", "carbs", "fats"]
GOAL_COLUMNS = [f"goal_{macro_nutrient}" for macro_nutrient in MACRO_NUTRIENTS]


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


class FoodEntry(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    food_name = models.TextField()
    total_calories = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    total_protein = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    total_fats = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    total_carbs = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    food_weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])

    def __str__(self):
        return f"{self.date} - {self.food_name} (Calories: {self.total_calories}, Protein: {self.total_protein}g, Fats: {self.total_fats}g, Carbs: {self.total_carbs}g, Weight: {self.food_weight}g)"
