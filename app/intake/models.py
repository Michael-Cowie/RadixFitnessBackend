from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
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
    total_calories = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    total_protein = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    total_fats = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    total_carbs = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    food_weight = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )

    def __str__(self):
        return (
            f"{self.date} - {self.food_name} "
            f"(Calories: {self.total_calories}, Protein: {self.total_protein}g, "
            f"Fats: {self.total_fats}g, Carbs: {self.total_carbs}g, Weight: {self.food_weight}g)"
        )
