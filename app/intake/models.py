from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class FoodEntry(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
        ordering = ["-date"]  # Most recent entries first by default

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    food_name = models.CharField(max_length=255)

    total_calories = models.FloatField(validators=[MinValueValidator(0)])
    total_protein = models.FloatField(validators=[MinValueValidator(0)])
    total_fats = models.FloatField(validators=[MinValueValidator(0)])
    total_carbs = models.FloatField(validators=[MinValueValidator(0)])
    food_weight = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return (
            f"{self.date} - {self.food_name} "
            f"(Calories: {self.total_calories}, Protein: {self.total_protein}g, "
            f"Fats: {self.total_fats}g, Carbs: {self.total_carbs}g, Weight: {self.food_weight}g)"
        )
