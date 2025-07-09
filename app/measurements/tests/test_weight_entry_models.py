from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from measurements.models import WeightEntry


class WeightTrackingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")

    def create_weight_entry(self, date, weight, user=None, notes=""):
        user = user or self.user
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        return WeightEntry.objects.create(date=date, weight_kg=weight, user=user, notes=notes)

    def test_creation_and_retrieval(self):
        weight = self.create_weight_entry("2024-01-06", 70.5)
        saved = WeightEntry.objects.get(id=weight.id)
        self.assertEqual(saved.date, datetime.strptime("2024-01-06", "%Y-%m-%d").date())
        self.assertEqual(saved.weight_kg, 70.5)
        self.assertEqual(saved.user, self.user)

    def test_string_representation(self):
        weight = self.create_weight_entry("2024-01-06", 70.5)
        expected = f"On {weight.date}, you weighed {weight.weight_kg}kg"
        self.assertEqual(str(weight), expected)
        self.assertEqual(str(weight), expected)

    def test_validation_fails_on_negative_weight(self):
        weight = self.create_weight_entry("2024-01-06", 70.5)
        weight.weight_kg = -5.0
        with self.assertRaises(ValidationError):
            weight.full_clean()

    def test_invalid_date_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.create_weight_entry("2024/01/06", 70.5)

    def test_filtering_by_specific_date(self):
        w1 = self.create_weight_entry("2024-01-06", 70.5)
        w2 = self.create_weight_entry("2024-01-07", 71)
        queryset = WeightEntry.objects.filter(date="2024-01-06")
        self.assertIn(w1, queryset)
        self.assertNotIn(w2, queryset)

    def test_weight_conversion_precision(self):
        kg_to_lbs = 2.2046226218488
        lbs = 165
        weight_kg = lbs / kg_to_lbs
        weight_entry = self.create_weight_entry("2024-01-01", weight_kg)
        restored_lbs = weight_entry.weight_kg * kg_to_lbs
        self.assertAlmostEqual(lbs, restored_lbs, places=5)

    def test_all_weights_belong_to_user(self):
        dates_weights = [
            ("2024-01-01", 70),
            ("2024-01-08", 71),
            ("2024-01-13", 72),
            ("2024-01-20", 73),
            ("2024-01-27", 74),
        ]
        created = [self.create_weight_entry(date, weight) for date, weight in dates_weights]
        weights = WeightEntry.objects.filter(user=self.user)
        for weight in created:
            self.assertIn(weight, weights)

    def test_notes_field_persistence(self):
        notes = "Going well, keep it up!"
        weight_entry = self.create_weight_entry("2024-01-01", 70, notes=notes)
        self.assertEqual(weight_entry.notes, notes)
