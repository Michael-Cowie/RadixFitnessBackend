from django.urls import path

from .views import *

urlpatterns = [
    path("", WeightsView.as_view(), name="weights"),
    path("all/", AllWeightsView.as_view(), name="all_weights"),
    path("goal_weight/", WeightGoalView.as_view(), name="goal_weight"),
]
