from django.contrib import admin

from goals.models import DailyMacronutrientGoal, WeightGoal
from goals.serializers import GOAL_COLUMNS


class IntakeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", *GOAL_COLUMNS)


admin.site.register(DailyMacronutrientGoal, IntakeAdmin)


class WeightGoalAdmin(admin.ModelAdmin):
    list_display = ("goal_date", "goal_weight_kg", "user")


admin.site.register(WeightGoal, WeightGoalAdmin)
