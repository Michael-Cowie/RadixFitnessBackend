from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import DailyIntakeTracking


class DailyIntakeTrackingTest(TestCase):
    """
    Test suite for the DailyIntakeTracking model.

    This test suite ensures that the DailyIntakeTracking model behaves as expected,
    including creation, validation, and string representation of the model instances.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for the test suite.

        This method creates a User instance to be used throughout the tests.
        """
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        """
        Set up data before each test case.

        This method retrieves the User instance created in setUpTestData
        and assigns it to an instance variable for use in individual tests.
        """
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
            current_calories=2000,
            goal_calories=2500,
            current_protein=150,
            goal_protein=200,
            current_carbs=300,
            goal_carbs=350,
            current_fats=70,
            goal_fats=80,
        )

        self.assertEqual(daily_intake.user_id, self.user)
        self.assertEqual(daily_intake.date, date.today())
        self.assertEqual(daily_intake.current_calories, 2000)
        self.assertEqual(daily_intake.goal_calories, 2500)
        self.assertEqual(daily_intake.current_protein, 150)
        self.assertEqual(daily_intake.goal_protein, 200)
        self.assertEqual(daily_intake.current_carbs, 300)
        self.assertEqual(daily_intake.goal_carbs, 350)
        self.assertEqual(daily_intake.current_fats, 70)
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
            current_calories=2000,
            goal_calories=2500,
            current_protein=150,
            goal_protein=200,
            current_carbs=300,
            goal_carbs=350,
            current_fats=70,
            goal_fats=80,
        )

        with self.assertRaises(ValidationError):
            duplicate_entry = DailyIntakeTracking(
                user_id=self.user,
                date=date.today(),
                current_calories=1800,
                goal_calories=2300,
                current_protein=140,
                goal_protein=190,
                current_carbs=280,
                goal_carbs=330,
                current_fats=65,
                goal_fats=75,
            )
            duplicate_entry.full_clean()  # This will trigger the unique constraint validation

    def test_max_value_validation(self):
        """
        Test that a ValidationError is raised when a value exceeds its maximum limit.

        This test checks the validation logic of the model, particularly ensuring that
        if the current_calories field exceeds the maximum allowed value of 5000, a
        ValidationError is raised. This test uses the full_clean() method to manually
        trigger model validation.
        """
        daily_intake = DailyIntakeTracking(
            user_id=self.user,
            date=date.today(),
            current_calories=6000,  # Invalid value, exceeds maximum allowed
            goal_calories=2500,
            current_protein=150,
            goal_protein=200,
            current_carbs=300,
            goal_carbs=350,
            current_fats=70,
            goal_fats=80,
        )

        with self.assertRaises(ValidationError):
            daily_intake.full_clean()

    def test_min_value_validation(self):
        """
        Test that a ValidationError is raised when a value is below its minimum limit.

        This test checks the validation logic of the model, ensuring that if the
        current_calories field is below the minimum allowed value of 0, a ValidationError
        is raised. This test also uses the full_clean() method to manually trigger model validation.
        """
        daily_intake = DailyIntakeTracking(
            user_id=self.user,
            date=date.today(),
            current_calories=-100,  # Invalid value, below minimum allowed
            goal_calories=2500,
            current_protein=150,
            goal_protein=200,
            current_carbs=300,
            goal_carbs=350,
            current_fats=70,
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
            current_calories=2000,
            goal_calories=2500,
            current_protein=150,
            goal_protein=200,
            current_carbs=300,
            goal_carbs=350,
            current_fats=70,
            goal_fats=80,
        )
        expected_str = f"""
        On {daily_intake.date} you have have the following intake,

        - Calories {daily_intake.current_calories} / {daily_intake.goal_calories}
        - Protein {daily_intake.current_protein} / {daily_intake.goal_protein}
        - Carbs {daily_intake.current_carbs} / {daily_intake.goal_carbs}
        - Fats {daily_intake.current_fats} / {daily_intake.goal_fats}
"""
        # Assert that the __str__ method returns the expected string
        self.assertEqual(str(daily_intake).strip(), expected_str.strip())
