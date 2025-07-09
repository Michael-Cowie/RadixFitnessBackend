from django.urls import path

from .views import *

WEIGHT_MEASUREMENTS_NAME = "weight-measurements"
WEIGHT_HISTORY_NAME = "weight-history"

urlpatterns = [
    path("weights/", WeightsView.as_view(), name=WEIGHT_MEASUREMENTS_NAME),
    path("weights/history/", AllWeightsView.as_view(), name=WEIGHT_HISTORY_NAME),
]
