from django.urls import path

from .views import MacronutrientAnalyticsView

MACRONUTRIENT_SUMMARY_NAME = "macronutrient-summary-analytics"

urlpatterns = [
    path("macronutrients/summary", MacronutrientAnalyticsView.as_view(), name=MACRONUTRIENT_SUMMARY_NAME),
]
