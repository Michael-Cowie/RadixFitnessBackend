# Generated by Django 4.2.7 on 2025-07-21 08:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0002_alter_dailymacronutrientgoal_goal_calories_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailymacronutrientgoal",
            name="goal_calories",
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name="dailymacronutrientgoal",
            name="goal_carbs",
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name="dailymacronutrientgoal",
            name="goal_fats",
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name="dailymacronutrientgoal",
            name="goal_protein",
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
