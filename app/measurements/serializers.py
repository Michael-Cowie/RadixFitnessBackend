from rest_framework.serializers import DateField, ModelSerializer, Serializer

from .models import WeightEntry


class WeightEntryRequestSerializer(ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ("date", "weight_kg", "notes")


class WeightEntryResponseSerializer(ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ("user", "date", "weight_kg", "notes")
        read_only_fields = fields


class WeightEntryDateSerializer(Serializer):
    date = DateField(required=True)
