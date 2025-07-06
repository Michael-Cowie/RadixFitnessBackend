from rest_framework.serializers import DateField, ModelSerializer, Serializer

from .models import WeightEntry


class WeightEntryRequestSerializer(ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ("date", "weight_kg", "notes")

    def create(self, validated_data):
        return WeightEntry.objects.create(user_id=self.context["user"], **validated_data)


class WeightEntryResponseSerializer(ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ("id", "user_id", "date", "weight_kg", "notes")
        read_only_fields = ("id", "user_id")


class WeightEntryDateSerializer(Serializer):
    date = DateField(required=True)
