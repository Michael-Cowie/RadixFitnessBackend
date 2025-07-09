from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from intake.models import FoodEntry
from intake.urls import FOOD_ENTRIES_NAME


class FoodEntryTrackingViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")
        cls.url = reverse(FOOD_ENTRIES_NAME)
        cls.base_food_entry_data = {
            "user": cls.user,
            "date": "2024-09-01",
            "food_name": "Test Food",
            "total_calories": "500.00",
            "total_protein": "30.00",
            "total_fats": "20.00",
            "total_carbs": "50.00",
            "food_weight": "200.00",
        }

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.food_entry = FoodEntry.objects.create(**self.base_food_entry_data)

    def test_get_food_entries_by_date(self):
        """GET should return entries for specified date."""
        response = self.client.get(self.url, {"date": self.base_food_entry_data["date"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        entry = response.data[0]
        for key in ("food_name", "total_calories", "total_protein", "total_fats", "total_carbs", "food_weight"):
            self.assertEqual(entry[key], self.base_food_entry_data[key])

    def test_get_food_entries_missing_date(self):
        """GET without date should return 400 with error."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
        self.assertIn("required", response.data["date"][0].lower())

    def test_get_food_entries_date_not_found(self):
        """GET for date with no entries returns 404 with detail message."""
        response = self.client.get(self.url, {"date": "2024-09-02"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail"), "No entries found for the given date.")

    def test_post_food_entry_success(self):
        """POST should create a new food entry with given data and date in query."""
        new_entry = {
            "food_name": "New Food",
            "total_calories": 600,
            "total_protein": 40,
            "total_fats": 25,
            "total_carbs": 60,
            "food_weight": 250,
        }
        response = self.client.post(
            self.url, data=new_entry, format="json", QUERY_STRING=f"date={self.base_food_entry_data['date']}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["food_name"], new_entry["food_name"])

    def test_post_food_entry_missing_date(self):
        """POST without date query param returns 400 error."""
        new_entry = {
            "food_name": "New Food",
            "total_calories": 600,
            "total_protein": 40,
            "total_fats": 25,
            "total_carbs": 60,
            "food_weight": 250,
        }
        response = self.client.post(self.url, data=new_entry, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
        self.assertIn("required", response.data["date"][0].lower())

    def test_patch_food_entry_success(self):
        """PATCH should update fields on food entry by id query param."""
        update_data = {"total_calories": "700.00", "total_protein": "50.00"}
        response = self.client.patch(self.url, data=update_data, format="json", QUERY_STRING=f"id={self.food_entry.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in update_data.items():
            self.assertEqual(response.data[k], v)

    def test_patch_food_entry_missing_id(self):
        """PATCH without id query param returns 400 error."""
        update_data = {"total_calories": 700, "total_protein": 50}
        response = self.client.patch(self.url, data=update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("id", response.data)
        self.assertIn("required", response.data["id"][0].lower())

    def test_patch_food_entry_not_found(self):
        """PATCH with non-existing id returns 404."""
        update_data = {"total_calories": 700, "total_protein": 50}
        response = self.client.patch(self.url, data=update_data, format="json", QUERY_STRING="id=999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail"), "Not found.")

    def test_delete_food_entry_success(self):
        """DELETE with valid id deletes the food entry."""
        response = self.client.delete(self.url, QUERY_STRING=f"id={self.food_entry.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FoodEntry.objects.filter(id=self.food_entry.id).exists())

    def test_delete_food_entry_missing_id(self):
        """DELETE without id query param returns 400 error."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("id", response.data)
        self.assertIn("required", response.data["id"][0].lower())

    def test_delete_food_entry_not_found(self):
        """DELETE with non-existing id returns 404."""
        response = self.client.delete(self.url, QUERY_STRING="id=999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail"), "Not found.")

    def test_delete_food_entry_another_users_entry(self):
        """DELETE with id of another user’s entry returns 404."""
        another_user = User.objects.create_user(username="hacker")
        self.client.force_authenticate(user=another_user)

        # Use existing entry id created by test user
        target_id = self.food_entry.id

        response = self.client.delete(self.url, QUERY_STRING=f"id={target_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail"), "Not found.")
