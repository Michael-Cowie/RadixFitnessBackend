from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer


def _get_profile(uid):
    try:
        return Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        raise Http404


class ProfileView(APIView):

    def post(self, request):
        """
        Create a UserProfile and add it to the database.
        """
        data = request.data | {'uid': request.user.username}
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Get a UserProfile.
        """
        user_profile = _get_profile(request.user.username)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)

    def patch(self, request):
        """
        Updates an existing UserProfile from the provided request data.
        """
        user_profile = _get_profile(request.user.username)
        serializer = ProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Delete a UserProfile.
        """
        user_profile = _get_profile(request.user.username)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
