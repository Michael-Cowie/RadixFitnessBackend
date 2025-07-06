from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodEntry
from .serializers import (
    FoodEntryDateQuerySerializer,
    FoodEntryIDQuerySerializer,
    FoodEntrySerializer,
)


class FoodEntryView(APIView):

    @staticmethod
    def _validate_query_params(serializer_class, request):
        serializer = serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            )
        ],
        responses={200: FoodEntrySerializer(many=True), 400: "Bad Request", 404: "Not Found"},
    )
    def get(self, request):
        validated_query_params = self._validate_query_params(FoodEntryDateQuerySerializer, request)

        entries = FoodEntry.objects.filter(user_id=request.user, date=validated_query_params["date"])
        if not entries.exists():
            return Response({"detail": "No entries found for the given date."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FoodEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=FoodEntrySerializer,
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            )
        ],
        responses={201: FoodEntrySerializer, 400: "Bad Request"},
    )
    def post(self, request):
        validated_query_params = self._validate_query_params(FoodEntryDateQuerySerializer, request)

        serializer = FoodEntrySerializer(
            data=request.data, context={"user": request.user, "date": validated_query_params["date"]}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=FoodEntrySerializer,
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="Entry ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: FoodEntrySerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def patch(self, request):
        validated_query_params = self._validate_query_params(FoodEntryIDQuerySerializer, request)

        entry = get_object_or_404(FoodEntry, id=validated_query_params["id"], user_id=request.user)

        serializer = FoodEntrySerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="Entry ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={204: "Entry deleted", 400: "Bad Request", 404: "Not Found"},
    )
    def delete(self, request):
        validated_query_params = self._validate_query_params(FoodEntryIDQuerySerializer, request)

        entry = get_object_or_404(FoodEntry, id=validated_query_params["id"], user_id=request.user)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
