from rest_framework.serializers import ModelSerializer

from .models import Weights, WeightGoal


class WeightTrackingResponse(ModelSerializer):
    class Meta:
        model = Weights
        fields = ('id', 'date', 'weight_kg', 'notes', 'user_id')


class WeightTrackingRequest(ModelSerializer):
    class Meta:
        model = Weights
        fields = ('date', 'weight_kg', 'notes')


class WeightTrackingForDate(ModelSerializer):
    class Meta:
        model = Weights
        fields = ('date', )


class WeightTrackingNoContent(ModelSerializer):
    class Meta:
        model = Weights
        fields = ()


class WeightGoalRequest(ModelSerializer):
    class Meta:
        model = WeightGoal
        fields = ('goal_date', 'goal_weight_kg')


class WeightGoalResponse(ModelSerializer):
    class Meta:
        model = WeightGoal
        fields = ('id', 'goal_date', 'goal_weight_kg', 'user_id')
