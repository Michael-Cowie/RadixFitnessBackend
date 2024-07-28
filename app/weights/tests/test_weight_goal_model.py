from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import WeightGoal


class WeightGoalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        self.user = User.objects.get(id=1)

    def _create_weight_goal_entry(self, goal_date, goal_weight_kg, user_id):
        return WeightGoal.objects.create(
            goal_date=goal_date, goal_weight_kg=goal_weight_kg, user_id=user_id
        )

    def test_basic_creation(self):
        goal_date = "2024-01-01"
        goal_weight = "70"
        model_entry = self._create_weight_goal_entry(goal_date, goal_weight, self.user)

        self.assertEqual(goal_date, model_entry.goal_date)
        self.assertEqual(goal_weight, model_entry.goal_weight_kg)

    def test_date_format(self):
        incorrect_goal_date_format = "2024-not-a-date"

        with self.assertRaises(ValidationError) as e:
            self._create_weight_goal_entry(incorrect_goal_date_format, 70, self.user)
        self.assertEqual(
            "['“2024-not-a-date” value has an invalid date format. It must be in YYYY-MM-DD format.']",
            str(e.exception),
        )

    def test_weight_validator(self):
        with self.assertRaises(ValidationError) as e:
            model_entry = self._create_weight_goal_entry("2024-01-01", 0, self.user)
            model_entry.full_clean()
        self.assertEqual(
            "[ValidationError(['Ensure this value is greater than or equal to 1.'])]",
            str(e.exception.error_dict["goal_weight_kg"]),
        )
