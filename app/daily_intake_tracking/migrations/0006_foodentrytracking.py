# Generated by Django 4.2.7 on 2024-09-01 12:56

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("daily_intake_tracking", "0005_alter_dailyintaketracking_current_calories_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FoodEntryTracking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("food_name", models.TextField()),
                (
                    "total_calories",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                (
                    "total_protein",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                (
                    "total_fats",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                (
                    "total_carbs",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                (
                    "food_weight",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]
