from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileRequestSerializer(ModelSerializer):
    """
    Serializer for creating and updating a user's profile.
    Does not allow setting the `user` via the request body;
    this is handled via context on the server.
    """

    class Meta:
        model = Profile
        fields = ("name", "measurement_system")

    def create(self, validated_data):
        return Profile.objects.create(user=self.context["user"], **validated_data)


class ProfileResponseSerializer(ModelSerializer):
    """
    Serializer for returning profile data to the client.
    Includes `id` and `user` for transparency.
    """

    class Meta:
        model = Profile
        fields = ("name", "measurement_system", "user")
        read_only_fields = fields


class ProfileNoContentSerializer(ModelSerializer):
    """
    Used as a placeholder schema for 204 No Content responses.
    """

    class Meta:
        model = Profile
        fields = ()
