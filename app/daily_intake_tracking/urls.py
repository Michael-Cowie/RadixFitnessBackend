from django.urls import path

from .views import DailyIntakeTrackingView

urlpatterns = [
    path(
        "macronutrient-progress/",
        DailyIntakeTrackingView.as_view(),
        name="macronutrient_date_progress",
    ),
]
