import json
from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import DailyIntakeTracking


class DailyIntakeTrackingViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        self.content_type = "application/json"
        self.user = User.objects.get(id=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = reverse("macronutrient_date_progress")

        # Create a daily intake tracking entry for testing
        self.test_data_date = "2024-08-24"
        self.test_data = {
            "user_id": self.user,
            "date": self.test_data_date,
            "current_calories": 1500,
            "goal_calories": 2000,
            "current_protein": 100,
            "goal_protein": 150,
            "current_carbs": 200,
            "goal_carbs": 250,
            "current_fats": 50,
            "goal_fats": 70,
        }
        DailyIntakeTracking.objects.create(**self.test_data)

    def _get_entry_for_user_on_date(self, user, user_date):
        return DailyIntakeTracking.objects.get(user_id=user, date=user_date)

    def test_create_daily_intake_tracking_success(self):
        """
        Test that a valid POST request successfully creates a DailyIntakeTracking entry.

        This test checks that when valid data is submitted via a POST request,
        a new DailyIntakeTracking entry is created, and the API responds with a
        201 Created status and the correct response data.
        """
        data = {
            "date": date.today().isoformat(),
            "current_calories": 2000,
            "goal_calories": 2500,
            "current_protein": 150,
            "goal_protein": 200,
            "current_carbs": 300,
            "goal_carbs": 350,
            "current_fats": 70,
            "goal_fats": 80,
        }

        response = self.client.post(
            self.url, json.dumps(data), content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        daily_intake_model_entry = self._get_entry_for_user_on_date(
            self.user, data["date"]
        )

        self.assertEqual(daily_intake_model_entry.user_id, self.user)
        self.assertEqual(daily_intake_model_entry.date.isoformat(), data["date"])
        self.assertEqual(
            daily_intake_model_entry.current_calories, data["current_calories"]
        )
        self.assertEqual(daily_intake_model_entry.goal_calories, data["goal_calories"])
        self.assertEqual(
            daily_intake_model_entry.current_protein, data["current_protein"]
        )
        self.assertEqual(daily_intake_model_entry.goal_protein, data["goal_protein"])
        self.assertEqual(daily_intake_model_entry.current_carbs, data["current_carbs"])
        self.assertEqual(daily_intake_model_entry.goal_carbs, data["goal_carbs"])
        self.assertEqual(daily_intake_model_entry.current_fats, data["current_fats"])
        self.assertEqual(daily_intake_model_entry.goal_fats, data["goal_fats"])

    def test_create_daily_intake_tracking_invalid_data(self):
        """
        Test that a POST request with invalid data returns a 400 Bad Request status.

        This test will attempt to pass current_calories with a value of 6000,
        passing the maximum of 5000. The test verifies that the POST does not add
        it to the model.
        """
        data = {
            "date": date.today().isoformat(),
            "current_calories": 6000,
            "goal_calories": 2500,
            "current_protein": 150,
            "goal_protein": 200,
            "current_carbs": 300,
            "goal_carbs": 350,
            "current_fats": 70,
            "goal_fats": 80,
        }

        response = self.client.post(
            self.url, json.dumps(data), content_type=self.content_type
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.assertRaises(DailyIntakeTracking.DoesNotExist):
            self._get_entry_for_user_on_date(self.user, data["date"])

        self.assertIn("current_calories", response.data)
        self.assertEqual(
            response.data["current_calories"][0],
            "Ensure this value is less than or equal to 5000.",
        )

    def test_create_daily_intake_tracking_unauthenticated(self):
        """
        Test that an unauthenticated POST request returns a 403 Forbidden status.

        This test checks that when an unauthenticated user attempts to create a
        DailyIntakeTracking entry via a POST request, the API responds with a
        403 Forbidden status.
        """
        self.client.logout()

        data = {
            "date": date.today().isoformat(),
            "current_calories": 2000,
            "goal_calories": 2500,
            "current_protein": 150,
            "goal_protein": 200,
            "current_carbs": 300,
            "goal_carbs": 350,
            "current_fats": 70,
            "goal_fats": 80,
        }

        response = self.client.post(
            self.url, json.dumps(data), content_type=self.content_type
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.assertRaises(DailyIntakeTracking.DoesNotExist):
            self._get_entry_for_user_on_date(self.user, data["date"])

    def test_get_daily_intake_valid_date(self):
        response = self.client.get(self.url, {"date": self.test_data_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in self.test_data.items():
            if key != "user_id":
                self.assertEqual(response.data[key], value)

    def test_get_daily_intake_invalid_date(self):
        response = self.client.get(self.url, {"date": "2024-08-26"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Entry not found")

    def test_get_daily_intake_no_date(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Date parameter is required")
