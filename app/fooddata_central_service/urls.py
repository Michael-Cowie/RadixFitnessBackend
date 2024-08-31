from django.urls import path

from .views import FoodSearchView

urlpatterns = [
    path("search/", FoodSearchView.as_view(), name="food-search"),
]
