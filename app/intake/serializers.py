from rest_framework.serializers import (
    DateField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from .models import FoodEntry


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
        fields = (
            "id",
            "user_id",
            "date",
            "food_name",
            "total_calories",
            "total_protein",
            "total_fats",
            "total_carbs",
            "food_weight",
        )
        read_only_fields = ("id", "user_id", "date")

    def create(self, validated_data):
        user = self.context["user"]
        date = self.context["date"]
        return FoodEntry.objects.create(user_id=user, date=date, **validated_data)


class FoodEntryDateQuerySerializer(Serializer):
    date = DateField(required=True)


class FoodEntryIDQuerySerializer(Serializer):
    id = IntegerField(required=True)
