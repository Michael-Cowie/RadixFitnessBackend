import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import DailyMacronutrientGoal
from ..urls import DAILY_MACRONUTRIENT_GOAL_NAME


class DailyIntakeTrackingViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        self.content_type = "application/json"
        self.user = User.objects.get(id=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = reverse(DAILY_MACRONUTRIENT_GOAL_NAME)

        self.test_data_date = "2024-08-24"
        self.test_data = {
            "user_id": self.user,
            "date": self.test_data_date,
            "goal_calories": 2000,
            "goal_protein": 150,
            "goal_carbs": 250,
            "goal_fats": 70,
        }
        DailyMacronutrientGoal.objects.create(**self.test_data)

    def _get_entry_for_user_on_date(self, user, user_date):
        return DailyMacronutrientGoal.objects.get(user_id=user, date=user_date)

    def test_get_daily_intake_valid_date(self):
        response = self.client.get(self.url, {"date": self.test_data_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in self.test_data.items():
            if key != "user_id":
                self.assertEqual(response.data[key], value)

    def test_get_daily_intake_invalid_date(self):
        response = self.client.get(self.url, {"date": "2024-08-26"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_get_daily_intake_no_date(self):
        response = self.client.get(self.url)

        self.assertIn("date", response.data)
        self.assertEqual(response.data["date"][0], "This field is required.")

    def test_put_update_daily_intake_tracking_success(self):
        """
        Test that a valid PUT request updates an existing DailyIntakeTracking entry and
        correctly returns a 200 OK status.
        """
        updated_data = {
            "date": self.test_data_date,
            "goal_calories": 2200,
            "goal_protein": 160,
            "goal_carbs": 260,
            "goal_fats": 75,
        }

        response = self.client.put(self.url, json.dumps(updated_data), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        daily_intake_model_entry = self._get_entry_for_user_on_date(self.user, updated_data["date"])

        self.assertEqual(daily_intake_model_entry.user_id, self.user)
        self.assertEqual(daily_intake_model_entry.goal_calories, updated_data["goal_calories"])
        self.assertEqual(daily_intake_model_entry.goal_protein, updated_data["goal_protein"])
        self.assertEqual(daily_intake_model_entry.goal_carbs, updated_data["goal_carbs"])
        self.assertEqual(daily_intake_model_entry.goal_fats, updated_data["goal_fats"])

    def test_put_create_new_daily_intake_tracking_success(self):
        """
        Test that a valid PUT request creates a new DailyIntakeTracking entry if it doesn't exist
        and correctly returns a 201 created status.
        """
        new_date = "2024-08-26"
        new_data = {
            "date": new_date,
            "goal_calories": 2500,
            "goal_protein": 200,
            "goal_carbs": 350,
            "goal_fats": 80,
        }

        response = self.client.put(self.url, json.dumps(new_data), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        daily_intake_model_entry = self._get_entry_for_user_on_date(self.user, new_data["date"])

        self.assertEqual(daily_intake_model_entry.user_id, self.user)
        self.assertEqual(daily_intake_model_entry.date.isoformat(), new_date)
        self.assertEqual(daily_intake_model_entry.goal_calories, new_data["goal_calories"])
        self.assertEqual(daily_intake_model_entry.goal_protein, new_data["goal_protein"])
