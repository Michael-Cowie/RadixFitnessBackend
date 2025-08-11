from rest_framework import serializers


class AnalyticsQuerySerializer(serializers.Serializer):
    start = serializers.DateField()
    end = serializers.DateField()

    def validate(self, attrs):
        if attrs["start"] > attrs["end"]:
            raise serializers.ValidationError("start must be on or before end")
        return attrs


class SummaryItemSerializer(serializers.Serializer):
    totalConsumed = serializers.FloatField()
    totalGoal = serializers.FloatField()
    percentageOfGoal = serializers.FloatField()
    averageConsumed = serializers.FloatField()


class SummarySerializer(serializers.Serializer):
    calories = SummaryItemSerializer()
    protein = SummaryItemSerializer()
    carbs = SummaryItemSerializer()
    fats = SummaryItemSerializer()


class AnalyticsResponseSerializer(serializers.Serializer):
    startDate = serializers.DateField()
    endDate = serializers.DateField()
    daysWithLogs = serializers.IntegerField()
    summary = SummarySerializer()
