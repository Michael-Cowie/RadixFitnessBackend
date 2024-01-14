from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Units, Weights


class WeightTrackingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username='Test User')

    def setUp(self):
        self.user = User.objects.get(id=1)

    def _create_weight_tracking_entry(self, date, weight, unit, user_id):
        return Weights.objects.create(
            date=date,
            weight=weight,
            unit=unit,
            user_id=user_id
        )

    def test_weight_tracking_model_creation(self):
        date = '2024-01-06'
        date_as_datetime = datetime.strptime(date, '%Y-%m-%d').date()
        weight = self._create_weight_tracking_entry('2024-01-06', 70.5, Units.KILOGRAM, self.user)

        # Retrieve the created instance from the database
        saved_weight_tracking = Weights.objects.get(id=weight.id)

        # Check if the saved instance matches the original values
        self.assertEqual(saved_weight_tracking.date, date_as_datetime)
        self.assertEqual(saved_weight_tracking.weight, 70.5)
        self.assertEqual(saved_weight_tracking.unit, Units.KILOGRAM)
        self.assertEqual(saved_weight_tracking.user_id, self.user)

    def test_weight_tracking_model_representation(self):
        weight = self._create_weight_tracking_entry('2024-01-06', 70.5, Units.KILOGRAM, self.user)

        # Check if the __repr__ method returns the expected string
        expected_repr = f'On {weight.date}, you weighed {weight.weight}{weight.unit}'
        self.assertEqual(str(weight), expected_repr)

    def test_weight_tracking_model_str_method(self):
        weight = self._create_weight_tracking_entry('2024-01-06', 70.5, Units.KILOGRAM, self.user)

        # Check if the __str__ method returns the expected string
        expected_str = f'On {weight.date}, you weighed {weight.weight}{weight.unit}'
        self.assertEqual(str(weight), expected_str)

    def test_weight_tracking_model_validation(self):
        # Try creating a WeightTracking instance with invalid weights
        with self.assertRaises(ValidationError):
            negative_weight = -5.0 # Negative weights is not allowed
            weight = self._create_weight_tracking_entry('2024-01-06', negative_weight, Units.KILOGRAM, self.user)
            weight.full_clean()

        # Try creating a WeightTracking instance with invalid date format
        with self.assertRaises(ValidationError):
            invalid_date_format = '2024/01/06'  # Invalid date format, using / instead of -
            weight = self._create_weight_tracking_entry(invalid_date_format, 70.5, Units.KILOGRAM, self.user)
            weight.full_clean()

    def test_weight_tracking_model_units_choices(self):
        # Try creating a WeightTracking instance with an invalid unit
        with self.assertRaises(ValidationError):
            invalid_unit = 'invalid_unit'
            weight = self._create_weight_tracking_entry('2024-01-06', 70.5, invalid_unit, self.user)
            weight.full_clean()

    def test_weight_tracking_model_filter_by_date(self):
        # Create WeightTracking instances for different dates
        weight_1 = self._create_weight_tracking_entry('2024-01-06', 70.5, Units.KILOGRAM, self.user)
        weight_2 = self._create_weight_tracking_entry('2024-01-07', 71, Units.KILOGRAM, self.user)

        # Filter WeightTracking instances by date
        queryset = Weights.objects.filter(date='2024-01-06')

        # Check if the queryset contains the expected instance
        self.assertIn(weight_1, queryset)
        self.assertNotIn(weight_2, queryset)

    def test_weight_tracking_model_decimal_places(self):
        # Try creating a WeightTracking instance with too many decimal places
        with self.assertRaises(ValidationError):
            invalid_weight = 70.555,  # Too many decimal places
            weight = self._create_weight_tracking_entry('2024-01-06', invalid_weight, Units.KILOGRAM, self.user)
            weight.full_clean()

    def test_weight_tracking_too_many_max_digits(self):
        with self.assertRaises(ValidationError):
            invalid_weight = 70000.0,  # Too many max digits
            weight = self._create_weight_tracking_entry('2024-01-06', invalid_weight, Units.POUND, self.user)
            weight.full_clean()

    def test_weight_tracking_all_dates_for_user(self):
        created_weights = [
            self._create_weight_tracking_entry('2024-01-01', 70, Units.KILOGRAM, self.user),
            self._create_weight_tracking_entry('2024-01-08', 71, Units.KILOGRAM, self.user),
            self._create_weight_tracking_entry('2024-01-13', 72, Units.KILOGRAM, self.user),
            self._create_weight_tracking_entry('2024-01-20', 73, Units.KILOGRAM, self.user),
            self._create_weight_tracking_entry('2024-01-27', 74, Units.KILOGRAM, self.user),
        ]

        for weight in Weights.objects.filter(user_id=self.user):
            self.assertIn(weight, created_weights)


