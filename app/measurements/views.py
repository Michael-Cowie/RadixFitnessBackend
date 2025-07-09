from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WeightEntry
from .serializers import (
    WeightEntryDateSerializer,
    WeightEntryRequestSerializer,
    WeightEntryResponseSerializer,
)


class WeightsView(APIView):

    @swagger_auto_schema(
        request_body=WeightEntryRequestSerializer,
        responses={
            200: openapi.Response(
                description="Successfully created or updated a weight entry",
                schema=WeightEntryResponseSerializer,
            ),
            400: "Invalid data to create or update Weight entry",
        },
    )
    def put(self, request):
        """Create or update a weight entry for a particular date."""
        serializer = WeightEntryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        weight_entry, created = WeightEntry.objects.update_or_create(
            user=request.user,
            date=serializer.validated_data["date"],
            defaults=serializer.validated_data,
        )

        response_serializer = WeightEntryResponseSerializer(weight_entry)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=WeightEntryDateSerializer,
        responses={
            204: openapi.Response(description="Successfully deleted the weight entry"),
            400: "Bad Request",
            404: "Weight entry not found",
        },
    )
    def delete(self, request):
        """Delete a weight entry for a particular date."""
        serializer = WeightEntryDateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        weight_entry = get_object_or_404(WeightEntry, user=request.user, date=serializer.validated_data["date"])
        weight_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllWeightsView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of all weight entries for the user",
                schema=WeightEntryResponseSerializer(many=True),
            )
        }
    )
    def get(self, request):
        """Return all weight entries for the authenticated user, ordered by date descending."""
        weights = WeightEntry.objects.filter(user=request.user)
        serializer = WeightEntryResponseSerializer(weights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
