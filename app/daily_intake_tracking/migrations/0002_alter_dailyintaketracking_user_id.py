# Generated by Django 4.2.7 on 2024-08-25 02:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("daily_intake_tracking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailyintaketracking",
            name="user_id",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
