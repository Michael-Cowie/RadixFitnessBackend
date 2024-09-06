from django.urls import path

from .views import DailyIntakeTrackingView, FoodEntryTrackingView

urlpatterns = [
    path(
        "macronutrient-progress/",
        DailyIntakeTrackingView.as_view(),
        name="macronutrient_date_progress",
    ),
    path("food-entries/", FoodEntryTrackingView.as_view(), name="food-entries"),
]
