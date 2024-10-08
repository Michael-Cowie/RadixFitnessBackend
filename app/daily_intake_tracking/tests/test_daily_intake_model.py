from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import DailyIntakeTracking


class DailyIntakeTrackingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_create_daily_intake_tracking(self):
        """
        Test that a DailyIntakeTracking instance can be created with valid data.

        This test ensures that a DailyIntakeTracking instance is correctly created
        and all fields are accurately set. The test verifies that the values assigned
        during creation match the expected values.
        """
        daily_intake = DailyIntakeTracking.objects.create(
            user_id=self.user,
            date=date.today(),
            goal_calories=2500,
            goal_protein=200,
            goal_carbs=350,
            goal_fats=80,
        )

        self.assertEqual(daily_intake.user_id, self.user)
        self.assertEqual(daily_intake.date, date.today())
        self.assertEqual(daily_intake.goal_calories, 2500)
        self.assertEqual(daily_intake.goal_protein, 200)
        self.assertEqual(daily_intake.goal_carbs, 350)
        self.assertEqual(daily_intake.goal_fats, 80)

    def test_unique_together_constraint(self):
        """
        Test the unique together constraint on the date and user_id fields.

        This test ensures that the unique constraint on the date and user_id fields is enforced.
        When attempting to create a second DailyIntakeTracking instance for the same
        user on the same date, a ValidationError should be raised.
        """
        DailyIntakeTracking.objects.create(
            user_id=self.user,
            date=date.today(),
            goal_calories=2500,
            goal_protein=200,
            goal_carbs=350,
            goal_fats=80,
        )

        with self.assertRaises(ValidationError):
            duplicate_entry = DailyIntakeTracking(
                user_id=self.user,
                date=date.today(),
                goal_calories=2300,
                goal_protein=190,
                goal_carbs=330,
                goal_fats=75,
            )
            duplicate_entry.full_clean()  # This will trigger the unique constraint validation

    def test_max_value_validation(self):
        """
        Test that a ValidationError is raised when a value exceeds its maximum limit.

        This test checks the validation logic of the model, particularly ensuring that
        if the goal_calories field exceeds the maximum allowed value of 5000, a
        ValidationError is raised. This test uses the full_clean() method to manually
        trigger model validation.
        """
        daily_intake = DailyIntakeTracking(
            user_id=self.user,
            date=date.today(),
            goal_calories=6000,  # Invalid value, exceeds maximum allowed
            goal_protein=200,
            goal_carbs=350,
            goal_fats=80,
        )

        with self.assertRaises(ValidationError):
            daily_intake.full_clean()

    def test_min_value_validation(self):
        """
        Test that a ValidationError is raised when a value is below its minimum limit.

        This test checks the validation logic of the model, ensuring that if the
        goal_calories field is below the minimum allowed value of 0, a ValidationError
        is raised. This test also uses the full_clean() method to manually trigger model validation.
        """
        daily_intake = DailyIntakeTracking(
            user_id=self.user,
            date=date.today(),
            goal_calories=-100,  # Invalid value, below minimum allowed
            goal_protein=200,
            goal_carbs=350,
            goal_fats=80,
        )

        with self.assertRaises(ValidationError):
            daily_intake.full_clean()

    def test_str_method(self):
        """
        This test ensures that the string representation of a DailyIntakeTracking
        instance is formatted correctly and includes all relevant information about
        the user's daily intake and goals.
        """
        daily_intake = DailyIntakeTracking.objects.create(
            user_id=self.user,
            date=date.today(),
            goal_calories=2500,
            goal_protein=200,
            goal_carbs=350,
            goal_fats=80,
        )
        expected_str = f"""
        On {daily_intake.date} you have have the following goals,

        - Goal calories {daily_intake.goal_calories}
        - Goal protein {daily_intake.goal_protein}
        - Goal carbs {daily_intake.goal_carbs}
        - Goal fats {daily_intake.goal_fats}
"""
        # Assert that the __str__ method returns the expected string
        self.assertEqual(str(daily_intake).strip(), expected_str.strip())
