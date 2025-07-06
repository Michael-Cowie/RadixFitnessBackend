from django.urls import path

from .views import *

WEIGHTS_NAME = "weight-list"
WEIGHT_HISTORY_NAME = "weight-history"

urlpatterns = [
    path("weights/", WeightsView.as_view(), name=WEIGHTS_NAME),
    path("weights/history/", AllWeightsView.as_view(), name=WEIGHT_HISTORY_NAME),
]
