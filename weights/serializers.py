from rest_framework.serializers import ModelSerializer

from .models import Weights


class WeightTrackingSerializer(ModelSerializer):
    class Meta:
        model = Weights
        fields = ('id', 'date', 'weight', 'unit', 'user_id')
