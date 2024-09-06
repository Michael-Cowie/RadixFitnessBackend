from django.contrib.auth.models import User
from django.test import TestCase

from ..models import FoodEntryTracking


class FoodEntryTrackingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(id=1, username="Test User")
        cls.test_data = [
            {
                "user_id": cls.user,
                "date": "2024-09-01",
                "food_name": "Test Food 1",
                "total_calories": 500,
                "total_protein": 30,
                "total_fats": 20,
                "total_carbs": 50,
                "food_weight": 200,
            },
            {
                "user_id": cls.user,
                "date": "2024-09-01",
                "food_name": "Test Food 2",
                "total_calories": 600,
                "total_protein": 40,
                "total_fats": 25,
                "total_carbs": 60,
                "food_weight": 250,
            },
        ]

    def setUp(self):
        self.food_entries = [FoodEntryTracking.objects.create(**entry) for entry in self.test_data]

    def test_food_entry_creation(self):
        entries = FoodEntryTracking.objects.filter(user_id=self.user, date="2024-09-01")
        for entry, data in zip(entries, self.test_data):
            self.assertEqual(entry.user_id, data["user_id"])
            self.assertEqual(entry.date.isoformat(), data["date"])
            self.assertEqual(entry.food_name, data["food_name"])
            self.assertEqual(entry.total_calories, data["total_calories"])
            self.assertEqual(entry.total_protein, data["total_protein"])
            self.assertEqual(entry.total_fats, data["total_fats"])
            self.assertEqual(entry.total_carbs, data["total_carbs"])
            self.assertEqual(entry.food_weight, data["food_weight"])

    def test_food_entry_str(self):
        expected_str = "2024-09-01 - Test Food 1 (Calories: 500, Protein: 30g, Fats: 20g, Carbs: 50g, Weight: 200g)"
        self.assertEqual(str(self.food_entries[0]), expected_str)
