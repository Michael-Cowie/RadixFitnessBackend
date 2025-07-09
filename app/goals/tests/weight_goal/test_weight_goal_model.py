from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from goals.models import WeightGoal


def _create_weight_goal_entry(goal_date, goal_weight_kg, user):
    return WeightGoal(goal_date=goal_date, goal_weight_kg=goal_weight_kg, user=user)


class WeightGoalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(id=1, username="Test User")

    def test_can_create_valid_weight_goal(self):
        """Test that a valid WeightGoal instance can be created and saved."""
        goal_date = date(2024, 1, 1)
        goal_weight = Decimal("70.0")

        entry = _create_weight_goal_entry(goal_date, goal_weight, self.user)
        entry.full_clean()  # Triggers validation
        entry.save()

        self.assertEqual(entry.goal_date, goal_date)
        self.assertEqual(entry.goal_weight_kg, goal_weight)
        self.assertEqual(entry.user, self.user)

    def test_invalid_date_format_raises_error(self):
        """Test that invalid date strings raise ValidationError when coerced improperly."""
        with self.assertRaises(ValidationError):
            # Django models expect a date object, not a string in the model directly
            _create_weight_goal_entry("2024-not-a-date", 70, self.user).full_clean()

    def test_goal_weight_must_be_greater_than_one(self):
        """Test that weight below 1.0 raises a validation error."""
        entry = _create_weight_goal_entry(date(2024, 1, 1), Decimal("0.0"), self.user)

        with self.assertRaises(ValidationError) as ctx:
            entry.full_clean()

        self.assertIn("goal_weight_kg", ctx.exception.error_dict)
        self.assertEqual(
            ctx.exception.messages[0],
            "Ensure this value is greater than or equal to 1.",
        )
