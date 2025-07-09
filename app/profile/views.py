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
        request_body=ProfileRequestSerializer,
        responses={201: ProfileResponseSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ProfileRequestSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(ProfileResponseSerializer(profile).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: ProfileResponseSerializer, 404: "Profile not found"},
    )
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        return Response(ProfileResponseSerializer(profile).data)

    @swagger_auto_schema(
        request_body=ProfileRequestSerializer,
        responses={200: ProfileResponseSerializer, 400: "Bad Request"},
    )
    def patch(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileRequestSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        profile = serializer.save()
        return Response(ProfileResponseSerializer(profile).data)

    @swagger_auto_schema(
        request_body=ProfileNoContentSerializer,
        responses={204: "Successfully deleted"},
    )
    def delete(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
