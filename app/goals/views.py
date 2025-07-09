from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DailyMacronutrientGoal, WeightGoal
from .serializers import (
    DailyMacronutrientGoalQuerySerializer,
    DailyMacronutrientGoalResponseSerializer,
    DailyMacronutrientGoalUpsertSerializer,
    WeightGoalRequestSerializer,
    WeightGoalResponseSerializer,
)


class DailyMacronutrientGoalView(APIView):

    @swagger_auto_schema(
        request_body=DailyMacronutrientGoalUpsertSerializer,
        responses={
            200: openapi.Response(
                description="Successfully updated the food tracking entry",
                schema=DailyMacronutrientGoalResponseSerializer,
            ),
            201: openapi.Response(
                description="Successfully created a food tracking entry",
                schema=DailyMacronutrientGoalResponseSerializer,
            ),
            400: "Invalid data for food tracking entry",
        },
    )
    def put(self, request):
        """
        Create or update an entry to track daily macronutrient intake for a particular date.
        """
        serializer = DailyMacronutrientGoalUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance, created = DailyMacronutrientGoal.objects.update_or_create(
            user=request.user,
            date=serializer.validated_data["date"],
            defaults=serializer.validated_data,
        )

        response_serializer = DailyMacronutrientGoalResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format="date",
                required=True,
                description="The date to retrieve macronutrient goal for (YYYY-MM-DD).",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successfully retrieved the macronutrient goal for the provided date",
                schema=DailyMacronutrientGoalResponseSerializer,
            ),
            400: "Bad request (missing or invalid date)",
            404: "Goal not found for given date",
        },
    )
    def get(self, request):
        """
        Retrieve the macronutrient goal for a specific user on a specific date.
        """
        query_serializer = DailyMacronutrientGoalQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        response_serializer = DailyMacronutrientGoalResponseSerializer(
            get_object_or_404(DailyMacronutrientGoal, user=request.user, date=query_serializer.validated_data["date"])
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class WeightGoalView(APIView):

    @swagger_auto_schema(
        request_body=WeightGoalRequestSerializer,
        responses={
            200: openapi.Response(
                description="Weight goal successfully created or updated.",
                schema=WeightGoalResponseSerializer,
            ),
            400: "Invalid input data.",
        },
    )
    def put(self, request):
        """
        Create or update the user's weight goal.
        """
        serializer = WeightGoalRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        goal, created = WeightGoal.objects.update_or_create(
            user=request.user,
            defaults=serializer.validated_data,
        )

        response_serializer = WeightGoalResponseSerializer(goal)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        """
        Retrieve the user's current weight goal.
        """
        serializer = WeightGoalResponseSerializer(get_object_or_404(WeightGoal, user=request.user))
        return Response(serializer.data, status=status.HTTP_200_OK)
