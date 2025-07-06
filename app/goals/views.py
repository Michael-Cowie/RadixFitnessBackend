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
    WeightGoalSerializer,
)


class DailyMacronutrientGoalView(APIView):

    @swagger_auto_schema(
        request_body=DailyMacronutrientGoalUpsertSerializer,
        responses={
            "200": openapi.Response(
                description="Successfully updated the food tracking entry",
            ),
            "201": openapi.Response(
                description="Successfully created a food tracking entry",
            ),
            "400": "Invalid data for food tracking entry",
        },
    )
    def put(self, request):
        """
        Create or update an entry to track daily macronutrient intake for a particular date.
        If an entry for the specified date already exists, it will be updated; otherwise, a new entry will be created.
        """
        serializer = DailyMacronutrientGoalUpsertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance, created = DailyMacronutrientGoal.objects.update_or_create(
            user_id=request.user,
            date=serializer.validated_data["date"],
            defaults=serializer.validated_data,
        )

        return Response(
            {"detail": "Created" if created else "Updated"},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

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
            get_object_or_404(
                DailyMacronutrientGoal, user_id=request.user, date=query_serializer.validated_data["date"]
            )
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class WeightGoalView(APIView):

    @swagger_auto_schema(
        request_body=WeightGoalSerializer,
        responses={
            "201": openapi.Response(
                description="Weight goal created",
                schema=WeightGoalSerializer,
            ),
            "400": "Invalid input",
        },
    )
    def post(self, request):
        """
        Create a weight goal for the authenticated user.
        """
        serializer = WeightGoalSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Retrieve the user's current weight goal.
        """
        goal = get_object_or_404(WeightGoal, user_id=request.user)
        serializer = WeightGoalSerializer(goal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=WeightGoalSerializer,
        responses={
            200: openapi.Response(
                description="Weight goal successfully updated.",
                schema=WeightGoalSerializer,
            ),
            400: "Invalid input data.",
        },
    )
    def patch(self, request):
        """
        Partially update the user's existing weight goal.
        """
        serializer = WeightGoalSerializer(
            get_object_or_404(WeightGoal, user_id=request.user),
            data=request.data,
            partial=True,
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
