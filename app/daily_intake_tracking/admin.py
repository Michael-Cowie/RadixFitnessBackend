from django.contrib import admin

from .models import (
    CURRENT_COLUMNS,
    GOAL_COLUMNS,
    DailyIntakeTracking,
    FoodEntryTracking,
)


class DailyIntakeTrackingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "date", *CURRENT_COLUMNS, *GOAL_COLUMNS)


class FoodEntryTrackingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "date",
        "food_name",
        "total_calories",
        "total_protein",
        "total_fats",
        "total_carbs",
        "food_weight",
    )


admin.site.register(DailyIntakeTracking, DailyIntakeTrackingAdmin)
admin.site.register(FoodEntryTracking, FoodEntryTrackingAdmin)
