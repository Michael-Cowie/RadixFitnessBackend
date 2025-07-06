from django.urls import path

from .views import FoodSearchView

FOOD_SEARCH_NAME = "food-search"

urlpatterns = [
    path("search/", FoodSearchView.as_view(), name=FOOD_SEARCH_NAME),
]
