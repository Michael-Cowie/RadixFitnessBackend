from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileNoContent, ProfileRequest, ProfileResponse


def _get_profile_for_user(user):
    try:
        return Profile.objects.get(user_id=user)
    except Profile.DoesNotExist:
        raise Http404


class ProfileView(APIView):

    @swagger_auto_schema(
        request_body=ProfileRequest,
        responses={
            "201": openapi.Response(
                description="Successfully created a profile for the user",
                schema=ProfileResponse,
            ),
            "400": "Unable to create profile",
        },
    )
    def post(self, request):
        """
        Create a UserProfile and add it to the database.
        """
        request_serializer = ProfileRequest(data=request.data)
        if request_serializer.is_valid():
            response_data = request.data | {"user_id": request.user.id}
            response_serializer = ProfileResponse(data=response_data)
            if response_serializer.is_valid():
                response_serializer.save()
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Get a profile for the logged-in user.
        """
        user_profile = _get_profile_for_user(request.user)
        serializer = ProfileResponse(user_profile)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProfileRequest,
        responses={
            "200": openapi.Response(
                description="Successfully updated a profile for the user",
                schema=ProfileResponse,
            ),
            "400": "Unable to update profile",
        },
    )
    def patch(self, request):
        """
        Updates an existing UserProfile from the provided request data.
        """
        user_profile = _get_profile_for_user(request.user)
        request_serializer = ProfileRequest(user_profile, data=request.data, partial=True)
        if request_serializer.is_valid():
            response_serializer = ProfileResponse(user_profile, request.data, partial=True)
            if response_serializer.is_valid():
                response_serializer.save()
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProfileNoContent,
        responses={"204": openapi.Response(description="Successfully deleted the profile", schema=ProfileNoContent)},
    )
    def delete(self, request):
        """
        Delete a UserProfile.
        """
        user_profile = _get_profile_for_user(request.user)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
