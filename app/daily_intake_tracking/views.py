from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DailyIntakeTracking
from .serializers import (
    CreateDailyIntakeTrackingRequest,
    DailyIntakeTrackingResponse,
    GetDailyIntakeTrackingRequest,
)


def _get_daily_intake_on_date(user, date):
    try:
        return DailyIntakeTracking.objects.get(user_id=user, date=date)
    except DailyIntakeTracking.DoesNotExist:
        raise Http404


class DailyIntakeTrackingView(APIView):

    @swagger_auto_schema(
        request_body=CreateDailyIntakeTrackingRequest,
        responses={
            "201": openapi.Response(
                description="Successfully created a food tracking entry",
            ),
            "400": "Invalid data to create food tracking entry",
        },
    )
    def post(self, request):
        """
        Create an entry to track daily macronutrient intake for a particular date.
        """
        request_serializer = CreateDailyIntakeTrackingRequest(data=request.data)
        if request_serializer.is_valid():
            request_serializer.save(user_id=request.user)

            return Response(status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=GetDailyIntakeTrackingRequest,
        responses={
            "201": openapi.Response(
                description="Successfully retrieved the macronutrient progress for the provided date",
            ),
            "404": "No entries",
        },
    )
    def get(self, request):
        """
        Retrieve the daily macronutrient intake for a particular date.
        """
        date = request.query_params.get("date")
        if not date:
            return Response(
                {"error": "Date parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            daily_intake = _get_daily_intake_on_date(request.user, date)
            response_data = DailyIntakeTrackingResponse(daily_intake).data
            return Response(response_data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"error": "Entry not found"}, status=status.HTTP_404_NOT_FOUND
            )
