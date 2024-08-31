import json
import os
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class FoodSearchViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        self.user = User.objects.get(id=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("food-search")

    @patch("fooddata_central_service.services.FoodDataCentralService.search_food")
    def test_search_food_success(self, mock_search_food):
        current_dir = os.path.dirname(__file__)

        with open(os.path.join(current_dir, "search_raw_chicken_breast.json")) as search_raw_chicken_breast:
            mock_search_food.return_value = json.loads(search_raw_chicken_breast.read())

        response = self.client.get(self.url, {"food": "Raw Chicken Breast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["search_query"], "Raw Chicken Breast")
        self.assertEqual(response.data["food_weight"], 100)
        self.assertEqual(response.data["food_unit"], "G")
        self.assertEqual(len(response.data["search_results"]), 10)

        # Define expected values for each food item
        expected_results = [
            {
                "description": "Chicken, broiler or fryers, breast, skinless, boneless, meat only, raw",
                "calories": {"value": 120, "unit": "KCAL"},
                "protein": {"value": 22.5, "unit": "G"},
                "fat": {"value": 2.62, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Chicken, broilers or fryers, breast, meat and skin, raw",
                "calories": {"value": 172, "unit": "KCAL"},
                "protein": {"value": 20.8, "unit": "G"},
                "fat": {"value": 9.25, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Chicken, broilers or fryers, breast, skinless, boneless, meat only, with added solution, raw",
                "calories": {"value": 108, "unit": "KCAL"},
                "protein": {"value": 20.3, "unit": "G"},
                "fat": {"value": 3.0, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Chicken, capons, giblets, raw",
                "calories": {"value": 130.14, "unit": "KCAL"},
                "protein": {"value": 18.3, "unit": "G"},
                "fat": {"value": 5.18, "unit": "G"},
                "carbs": {"value": 1.42, "unit": "G"},
            },
            {
                "description": "Chicken, ground, raw",
                "calories": {"value": 143, "unit": "KCAL"},
                "protein": {"value": 17.4, "unit": "G"},
                "fat": {"value": 8.1, "unit": "G"},
                "carbs": {"value": 0.04, "unit": "G"},
            },
            {
                "description": "Duck, wild, breast, meat only, raw",
                "calories": {"value": 123.21, "unit": "KCAL"},
                "protein": {"value": 19.8, "unit": "G"},
                "fat": {"value": 4.25, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Pheasant, breast, meat only, raw",
                "calories": {"value": 133.01, "unit": "KCAL"},
                "protein": {"value": 24.4, "unit": "G"},
                "fat": {"value": 3.25, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Quail, breast, meat only, raw",
                "calories": {"value": 123.21, "unit": "KCAL"},
                "protein": {"value": 22.6, "unit": "G"},
                "fat": {"value": 2.99, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Ruffed Grouse, breast meat, skinless, raw",
                "calories": {"value": 112, "unit": "KCAL"},
                "protein": {"value": 25.9, "unit": "G"},
                "fat": {"value": 0.88, "unit": "G"},
                "carbs": {"value": 0.0, "unit": "G"},
            },
            {
                "description": "Turkey, whole, breast, meat only, raw",
                "calories": {"value": 114, "unit": "KCAL"},
                "protein": {"value": 23.7, "unit": "G"},
                "fat": {"value": 1.48, "unit": "G"},
                "carbs": {"value": 0.14, "unit": "G"},
            },
        ]

        self.assertEqual(len(response.data["search_results"]), len(expected_results))

        for expected, actual in zip(expected_results, response.data["search_results"]):
            self.assertEqual(expected["description"], actual["description"])
            self.assertEqual(expected["calories"], actual["calories"])
            self.assertEqual(expected["protein"], actual["protein"])
            self.assertEqual(expected["fat"], actual["fat"])
            self.assertEqual(expected["carbs"], actual["carbs"])

    def test_search_food_missing_query_param(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Query parameter is required")

    @patch("fooddata_central_service.services.FoodDataCentralService.search_food")
    def test_search_food_no_results(self, mock_search_food):
        # Mock the service response with no foods found
        mock_search_food.return_value = {"foods": []}

        response = self.client.get(self.url, {"food": "unknownfood"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "No foods found")
