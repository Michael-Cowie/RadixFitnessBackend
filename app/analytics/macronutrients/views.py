from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from goals.models import DailyMacronutrientGoal
from intake.models import FoodEntry

from .serializers import AnalyticsQuerySerializer, AnalyticsResponseSerializer


def _default_payload(start, end):
    zero_item = {
        "totalConsumed": 0.0,
        "totalGoal": 0.0,
        "percentageOfGoal": 0.0,
        "averageConsumed": 0.0,
    }
    return {
        "startDate": start,
        "endDate": end,
        "daysWithLogs": 0,
        "summary": {
            "calories": dict(zero_item),
            "protein": dict(zero_item),
            "carbs": dict(zero_item),
            "fats": dict(zero_item),
        },
    }


class MacronutrientAnalyticsView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("start", openapi.IN_QUERY, type=openapi.TYPE_STRING, format="date", required=True),
            openapi.Parameter("end", openapi.IN_QUERY, type=openapi.TYPE_STRING, format="date", required=True),
        ],
        responses={200: openapi.Response("Analytics", AnalyticsResponseSerializer)},
    )
    def get(self, request):
        query = AnalyticsQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)

        start = query.validated_data["start"]
        end = query.validated_data["end"]

        entries_qs = FoodEntry.objects.filter(user=request.user, date__range=(start, end))
        days_with_logs = entries_qs.values("date").distinct().count()

        if days_with_logs == 0:
            payload = _default_payload(start, end)
            return Response(AnalyticsResponseSerializer(payload).data, status=status.HTTP_200_OK)

        goals_qs = DailyMacronutrientGoal.objects.filter(user=request.user, date__range=(start, end))

        consumed_totals = entries_qs.aggregate(
            calories=Sum("total_calories"),
            protein=Sum("total_protein"),
            carbs=Sum("total_carbs"),
            fats=Sum("total_fats"),
        )

        goal_totals = goals_qs.aggregate(
            calories=Sum("goal_calories", default=0),
            protein=Sum("goal_protein", default=0),
            carbs=Sum("goal_carbs", default=0),
            fats=Sum("goal_fats", default=0),
        )

        summary = {
            nutrient: {
                "totalConsumed": consumed_totals[nutrient],
                "totalGoal": goal_totals[nutrient],
                "percentageOfGoal": (
                    0 if goal_totals[nutrient] == 0 else (consumed_totals[nutrient] / goal_totals[nutrient]) * 100
                ),
                "averageConsumed": consumed_totals[nutrient] / days_with_logs,
            }
            for nutrient in ["calories", "protein", "carbs", "fats"]
        }

        payload = {
            "startDate": start,
            "endDate": end,
            "daysWithLogs": days_with_logs,
            "summary": summary,
        }

        return Response(AnalyticsResponseSerializer(payload).data, status=status.HTTP_200_OK)
