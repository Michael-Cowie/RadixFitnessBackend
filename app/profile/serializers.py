from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileRequestSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ("name", "measurement_system")


class ProfileResponseSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ("name", "measurement_system")
        read_only_fields = fields


class ProfileNoContentSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ()
