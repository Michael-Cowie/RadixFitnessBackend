from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileResponse(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'preferred_unit', 'user_id')


class ProfileRequest(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'preferred_unit')


class ProfileNoContent(ModelSerializer):
    class Meta:
        model = Profile
        fields = ()
