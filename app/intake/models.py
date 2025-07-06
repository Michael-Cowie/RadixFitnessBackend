from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
