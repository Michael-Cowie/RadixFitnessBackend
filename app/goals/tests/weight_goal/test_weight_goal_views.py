import json
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from goals.models import WeightGoal


def _date_as_datetime(date_str):
    """Convert YYYY-MM-DD string to a datetime.date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


class WeightGoalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(id=1, username="Test User")
        cls.test_url = reverse("goal_weight")

        WeightGoal.objects.create(
            user=cls.user,
            goal_date="2025-01-01",
            goal_weight_kg=70,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def _create_and_authenticate_user(self, user_id: int) -> User:
        """
        Creates and authenticates a new test user with the given ID.
        Useful for avoiding clashes with pre-created test data.
        """
        new_user = User.objects.create(id=user_id, username=f"Test User {user_id}")
        self.client.force_authenticate(user=new_user)
        return new_user

    def test_basic_get_response_matches_model(self):
        """Test that GET response returns the correct model data."""
        response = self.client.get(self.test_url)
        response_data = response.data

        model_entry = WeightGoal.objects.get(user=self.user)
        self.assertEqual(model_entry.goal_date, _date_as_datetime(response_data["goal_date"]))
        self.assertEqual(f"{model_entry.goal_weight_kg:.2f}", response_data["goal_weight_kg"])

    def test_basic_creation_for_new_user(self):
        """Test creating a new weight goal for a user who has no existing goal."""
        new_user = self._create_and_authenticate_user(user_id=2)

        goal_date = "2025-01-01"
        goal_weight = "70.00"
        request_data = json.dumps({"goal_date": goal_date, "goal_weight_kg": goal_weight})

        response = self.client.put(self.test_url, data=request_data, content_type="application/json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(goal_date, response_data["goal_date"])
        self.assertEqual(goal_weight, response_data["goal_weight_kg"])

        model_entry = WeightGoal.objects.get(user=new_user)
        self.assertEqual(model_entry.goal_date, _date_as_datetime(goal_date))
        self.assertEqual(Decimal(goal_weight), model_entry.goal_weight_kg)

    def test_update_goal_date(self):
        """Test updating the goal_date for an existing entry."""
        new_goal_date = "2026-01-01"
        request_data = json.dumps({"goal_date": new_goal_date, "goal_weight_kg": "70.00"})

        response = self.client.put(self.test_url, data=request_data, content_type="application/json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_goal_date, response_data["goal_date"])
        self.assertEqual("70.00", response_data["goal_weight_kg"])

        model_entry = WeightGoal.objects.get(user=self.user)
        self.assertEqual(model_entry.goal_date, _date_as_datetime(new_goal_date))

    def test_update_goal_weight(self):
        """Test updating the goal_weight_kg for an existing entry."""
        new_goal_weight = "100.00"
        request_data = json.dumps(
            {
                "goal_date": "2025-01-01",
                "goal_weight_kg": new_goal_weight,
            }
        )

        response = self.client.put(self.test_url, data=request_data, content_type="application/json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_goal_weight, response_data["goal_weight_kg"])

        model_entry = WeightGoal.objects.get(user=self.user)
        self.assertEqual(Decimal(new_goal_weight), model_entry.goal_weight_kg)
