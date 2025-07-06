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
    """

    class Meta:
        model = DailyMacronutrientGoal
        fields = ("date", *GOAL_COLUMNS)
        read_only_fields = fields


class WeightGoalSerializer(ModelSerializer):
    class Meta:
        model = WeightGoal
        fields = ("id", "goal_date", "goal_weight_kg")
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["user_id"] = self.context["user"]
        return super().create(validated_data)
