import json
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import WeightGoal


class WeightGoalTest(TestCase):

    def date_as_datetime(self, date):
        return datetime.strptime(date, "%Y-%m-%d").date()

    def setUp(self):
        self.test_url = reverse("goal_weight")

        self.content_type = "application/json"
        self.user = User.objects.get(id=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(id=1, username="Test User")

        WeightGoal.objects.create(
            goal_date="2025-01-01", goal_weight_kg=70, user_id=user
        )

    def test_basic_response(self):
        response_data = self.client.get(self.test_url).data

        model_entry = WeightGoal.objects.get(id=1)
        self.assertEqual(
            model_entry.goal_date, self.date_as_datetime(response_data["goal_date"])
        )
        self.assertEqual(model_entry.goal_weight_kg, response_data["goal_weight_kg"])

    def test_basic_creation(self):
        goal_date = "2025-01-01"
        goal_weight_kg = 70
        request_data = json.dumps(
            {"goal_date": goal_date, "goal_weight_kg": goal_weight_kg}
        )

        response = self.client.post(
            self.test_url, data=request_data, content_type=self.content_type
        )
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(goal_date, response_data["goal_date"])
        self.assertEqual(goal_weight_kg, response_data["goal_weight_kg"])

    def test_patch_date(self):
        new_goal_date = "2026-01-01"
        request_data = json.dumps(
            {
                "goal_date": new_goal_date,
            }
        )

        response = self.client.patch(
            self.test_url, data=request_data, content_type=self.content_type
        )
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_goal_date, response_data["goal_date"])
        self.assertEqual(70, response_data["goal_weight_kg"])

        model_entry = WeightGoal.objects.get(id=1)
        self.assertEqual(self.date_as_datetime(new_goal_date), model_entry.goal_date)

    def test_patch_weight(self):
        new_goal_weight = 100
        request_data = json.dumps(
            {
                "goal_weight_kg": new_goal_weight,
            }
        )

        response = self.client.patch(
            self.test_url, data=request_data, content_type=self.content_type
        )
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_goal_weight, response_data["goal_weight_kg"])
        self.assertEqual(100, response_data["goal_weight_kg"])

        model_entry = WeightGoal.objects.get(id=1)
        self.assertEqual(new_goal_weight, model_entry.goal_weight_kg)
