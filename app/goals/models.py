from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class DailyMacronutrientGoal(models.Model):
    class Meta:
        unique_together = ("date", "user")
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
        ordering = ["-date"]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    goal_calories = models.FloatField(validators=[MinValueValidator(0)])
    goal_protein = models.FloatField(validators=[MinValueValidator(0)])
    goal_carbs = models.FloatField(validators=[MinValueValidator(0)])
    goal_fats = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"""
        On {self.date} you have the following goals,

        - Goal calories - {self.goal_calories} kcal
        - Goal protein - {self.goal_protein} g
        - Goal carbs - {self.goal_carbs} g
        - Goal fats - {self.goal_fats} g
        """


class WeightGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    goal_date = models.DateField()
    goal_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"I want to be {self.goal_weight_kg} by {self.goal_date}"
