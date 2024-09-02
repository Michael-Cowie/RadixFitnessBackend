from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import (
    CURRENT_COLUMNS,
    GOAL_COLUMNS,
    DailyIntakeTracking,
    FoodEntryTracking,
)


class FoodEntryTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEntryTracking
        fields = "__all__"


class CreateDailyIntakeTrackingRequest(ModelSerializer):
    class Meta:
        model = DailyIntakeTracking
        fields = ("date", *CURRENT_COLUMNS, *GOAL_COLUMNS)


class GetDailyIntakeTrackingRequest(ModelSerializer):
    class Meta:
        model = DailyIntakeTracking
        fields = ("date",)


class DailyIntakeTrackingResponse(ModelSerializer):
    class Meta:
        model = DailyIntakeTracking
        fields = ("date", *CURRENT_COLUMNS, *GOAL_COLUMNS)
