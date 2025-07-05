from django.urls import path

from .views import DailyMacronutrientGoalView, FoodEntryTrackingView

DAILY_MACRONUTRIENT_GOAL_NAME = "daily_macronutrient_goal"
FOOD_ENTRIES_NAME = "food-entries"

urlpatterns = [
    path(
        "macronutrient-progress/",
        DailyMacronutrientGoalView.as_view(),
        name=DAILY_MACRONUTRIENT_GOAL_NAME,
    ),
    path("food-entries/", FoodEntryTrackingView.as_view(), name="food-entries"),
]
