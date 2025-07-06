from django.urls import path

from .views import FoodEntryView

FOOD_ENTRIES_NAME = "food-entries"

urlpatterns = [path("foods/", FoodEntryView.as_view(), name=FOOD_ENTRIES_NAME)]
