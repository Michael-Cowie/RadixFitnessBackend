from rest_framework.serializers import DateField, ModelSerializer, Serializer

from goals.models import DailyMacronutrientGoal, WeightGoal

MACRO_NUTRIENTS = ["calories", "protein", "carbs", "fats"]
GOAL_COLUMNS = [f"goal_{macro_nutrient}" for macro_nutrient in MACRO_NUTRIENTS]


class DailyMacronutrientGoalUpsertSerializer(ModelSerializer):
    """
    Used to create or update daily intake tracking entries.
    """

    class Meta:
        model = DailyMacronutrientGoal
        fields = ("date", *GOAL_COLUMNS)


class DailyMacronutrientGoalQuerySerializer(Serializer):
    """
    Serializer for validating the `date` query parameter used to retrieve a user's
    macronutrient goal for a specific day.
    """

    date = DateField()


class DailyMacronutrientGoalResponseSerializer(ModelSerializer):
    """
    Serializer to output the daily macronutrient goal data for a user.
    Read-only serializer - no validation or saving logic.
    """

    class Meta:
        model = DailyMacronutrientGoal
        fields = ("date", *GOAL_COLUMNS)
        read_only_fields = fields


class WeightGoalRequestSerializer(ModelSerializer):
    """
    Serializer for creating and updating weight goals.

    Does not allow setting the `user` via the request body, this is handled via context on the server.
    """

    class Meta:
        model = WeightGoal
        fields = ("goal_date", "goal_weight_kg")


class WeightGoalResponseSerializer(ModelSerializer):
    """
    Serializer for outputting weight goal data.
    """

    class Meta:
        model = WeightGoal
        fields = ("goal_date", "goal_weight_kg")
        read_only_fields = fields
