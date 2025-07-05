from rest_framework.serializers import ModelSerializer, Serializer, DateField, IntegerField

from .models import GOAL_COLUMNS, DailyMacronutrientGoal, FoodEntry


class FoodEntrySerializer(ModelSerializer):
    """
    Serializer for the FoodEntry model.

    Handles serialization and deserialization of FoodEntry instances.

    - During creation, the `user_id` and `date` fields are injected via the serializer context
      to ensure these fields are set server-side and cannot be modified by the client.
    - The `id`, `user_id`, and `date` fields are marked read-only to prevent client modification.
    - On successful creation, the serializer returns the new FoodEntry instance including its `id`.
      This `id` can be used in subsequent PATCH requests to update the entry.
    """
    class Meta:
        model = FoodEntry
        fields = "__all__"
        read_only_fields = ("id", "user_id", "date")

    def create(self, validated_data):
        user = self.context["user"]
        date = self.context["date"]
        return FoodEntry.objects.create(user_id=user, date=date, **validated_data)

class FoodEntryDateQuerySerializer(Serializer):
    date = DateField(required=True)

class FoodEntryIDQuerySerializer(Serializer):
    id = IntegerField(required=True)


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
