from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import WeightEntry
from ..urls import WEIGHT_HISTORY_NAME, WEIGHT_MEASUREMENTS_NAME


def date_as_datetime(date: str):
    return datetime.strptime(date, "%Y-%m-%d").date()


class BaseWeightEntryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        cls.initial_entries = [
            ("2024-01-01", 70),
            ("2024-01-08", 71),
            ("2024-01-13", 72),
            ("2024-01-20", 73),
            ("2024-01-27", 74),
            ("2024-02-01", 163),
            ("2024-02-08", 167.5),
            ("2024-02-15", 171.33),
        ]

        for date, weight in cls.initial_entries:
            WeightEntry.objects.create(user=cls.user, date=date, weight_kg=weight)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.user = User.objects.get(username="testuser")


class AllWeightsViewTest(BaseWeightEntryTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse(WEIGHT_HISTORY_NAME)
        self.response = self.client.get(self.url)
        self.data = self.response.data

    def test_returns_correct_data(self):
        """Should return all weight entries for the authenticated user"""
        for entry in self.data:
            with self.subTest(date=entry["date"]):
                obj = WeightEntry.objects.get(user_id=entry["user"], date=entry["date"])
                self.assertEqual(entry["weight_kg"], obj.weight_kg)
                self.assertEqual(entry["user"], obj.user.id)

    def test_returns_correct_number_of_entries(self):
        """Should return the expected number of weight entries"""
        self.assertEqual(len(self.data), len(self.initial_entries))

    def test_empty_response_for_new_user(self):
        """Should return an empty list for a user with no weight entries"""
        new_user = User.objects.create_user(username="emptyuser", password="test")
        self.client.force_authenticate(user=new_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_dates_returned_in_descending_order(self):
        """Dates should be returned in descending order (most recent first)"""
        new_user = User.objects.create_user(username="ordereduser", password="test")
        self.client.force_authenticate(user=new_user)

        unsorted_dates = [
            "2024-01-01",
            "2024-01-02",
            "2024-05-01",
            "2024-08-16",
            "2024-09-17",
            "2024-12-20",
            "2024-12-25",
            "2023-12-25",
            "2023-05-18",
        ]

        for i, date in enumerate(reversed(unsorted_dates)):  # Insert in reverse order
            WeightEntry.objects.create(user=new_user, date=date, weight_kg=50 + i)

        response = self.client.get(self.url)
        response_dates = [entry["date"] for entry in response.data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_dates, sorted(unsorted_dates, reverse=True))


class WeightMeasurementTest(BaseWeightEntryTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse(WEIGHT_MEASUREMENTS_NAME)
        self.date = "2000-01-01"
        self.weight = 200.0
        self.payload = {"date": self.date, "weight_kg": self.weight}

    def test_can_create_weight_entry(self):
        """Should create a new weight entry"""
        response = self.client.put(self.url, data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], self.date)
        self.assertEqual(response.data["weight_kg"], self.weight)

    def test_can_update_existing_weight(self):
        """Should update an existing weight entry"""
        self.client.put(self.url, data=self.payload, format="json")

        updated_weight = 230
        response = self.client.put(self.url, data={"date": self.date, "weight_kg": updated_weight}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_entry = WeightEntry.objects.get(user=self.user, date=self.date)
        self.assertEqual(updated_entry.weight_kg, updated_weight)

    def test_can_update_notes_field(self):
        """Should update notes for an existing weight entry"""
        initial_notes = "Initial note"
        self.client.put(self.url, data={**self.payload, "notes": initial_notes}, format="json")

        new_notes = "Updated note"
        response = self.client.put(self.url, data={**self.payload, "notes": new_notes}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["notes"], new_notes)

    def test_can_delete_weight_entry(self):
        """Should delete an existing weight entry"""
        self.client.put(self.url, data=self.payload, format="json")

        response = self.client.delete(self.url, data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        exists = WeightEntry.objects.filter(user=self.user, date=self.date).exists()
        self.assertFalse(exists)
