from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileResponse(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "name", "measurement_system", "user_id")


class ProfileRequest(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("name", "measurement_system")


class ProfileNoContent(ModelSerializer):
    class Meta:
        model = Profile
        fields = ()
