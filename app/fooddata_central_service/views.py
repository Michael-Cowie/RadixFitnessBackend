from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FoodSearchResultSerializer
from .services import FoodDataCentralService


class FoodSearchView(APIView):

    @swagger_auto_schema(
        operation_description="Search for foods using a query parameter 'food'. Returns a list of matching foods with "
        "their nutritional information.",
        manual_parameters=[
            openapi.Parameter(
                "food",
                openapi.IN_QUERY,
                description="The name of the food to search for.",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="A list of foods matching the search query with nutritional details.",
                examples={
                    "application/json": {
                        "food_weight": 100,
                        "food_unit": "G",
                        "search_query": "apple",
                        "search_results": [
                            {
                                "description": "Apple, raw",
                                "calories": [52, "KCAL"],
                                "protein": [0.26, "G"],
                                "fat": [0.17, "G"],
                                "carbs": [13.81, "G"],
                            }
                        ],
                    }
                },
            ),
            400: openapi.Response(
                description="Bad request. Query parameter is missing.",
            ),
            404: openapi.Response(description="No foods found matching the search query."),
        },
    )
    def get(self, request):
        search_food = request.query_params.get("food", None)
        if not search_food:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if search_results := FoodDataCentralService.get_foods_by_query_name(search_food):
            response_data = {
                "food_weight": 100,
                "food_unit": "G",
                "search_query": search_food,
                "search_results": [FoodSearchResultSerializer(food).data for food in search_results],
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "No foods found"}, status=status.HTTP_404_NOT_FOUND)
