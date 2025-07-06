from django.urls import path

from .views import DailyMacronutrientGoalView, WeightGoalView

DAILY_MACRONUTRIENT_GOAL_NAME = "daily_macronutrient_goal"
GOAL_WEIGHT_NAME = "goal_weight"

urlpatterns = [
    path(
        "macronutrient/daily/",
        DailyMacronutrientGoalView.as_view(),
        name=DAILY_MACRONUTRIENT_GOAL_NAME,
    ),
    path("weight/", WeightGoalView.as_view(), name=GOAL_WEIGHT_NAME),
]
