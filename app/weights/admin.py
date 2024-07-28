from django.contrib import admin

from .models import WeightGoal, Weights


class WeightsAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "weight_kg", "user_id")


class WeightGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "goal_date", "goal_weight_kg", "user_id")


admin.site.register(Weights, WeightsAdmin)
admin.site.register(WeightGoal, WeightGoalAdmin)
