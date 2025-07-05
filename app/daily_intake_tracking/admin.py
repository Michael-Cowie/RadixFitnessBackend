from django.contrib import admin

from .models import GOAL_COLUMNS, DailyMacronutrientGoal, FoodEntry


class DailyIntakeTrackingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "date", *GOAL_COLUMNS)


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


admin.site.register(DailyMacronutrientGoal, DailyIntakeTrackingAdmin)
admin.site.register(FoodEntry, FoodEntryTrackingAdmin)
