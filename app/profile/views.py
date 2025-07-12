from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import (
    ProfileNoContentSerializer,
    ProfileRequestSerializer,
    ProfileResponseSerializer,
)


class ProfileView(APIView):

    @swagger_auto_schema(
        responses={200: ProfileResponseSerializer, 404: "Profile not found"},
    )
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        return Response(ProfileResponseSerializer(profile).data)

    @swagger_auto_schema(responses={200: ProfileResponseSerializer, 404: "Profile not found"})
    def put(self, request):
        serializer = ProfileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance, created = Profile.objects.update_or_create(
            user=request.user,
            defaults=serializer.validated_data,
        )

        response_serializer = ProfileResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProfileNoContentSerializer,
        responses={204: "Successfully deleted"},
    )
    def delete(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
