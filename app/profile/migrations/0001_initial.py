# Generated by Django 4.2.7 on 2024-03-29 05:34

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-Z]+$",
                                "Only alpha characters of length 1 or more are accepted",
                            )
                        ]
                    ),
                ),
                (
                    "measurement_system",
                    models.CharField(
                        choices=[("Metric", "Metric"), ("Imperial", "Imperial")],
                        max_length=8,
                    ),
                ),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
