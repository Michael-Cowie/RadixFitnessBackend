from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import FoodEntryTracking
import json


class FoodEntryTrackingViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(id=1)
        cls.content_type = "application/json"
        cls.url = reverse("food-entries")
        cls.test_data = {
            "user_id": cls.user,
            "date": "2024-09-01",
            "food_name": "Test Food",
            "total_calories": 500,
            "total_protein": 30,
            "total_fats": 20,
            "total_carbs": 50,
            "food_weight": 200,
        }

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.food_entry = FoodEntryTracking.objects.create(**self.test_data)

    def test_get_food_entries_by_date(self):
        response = self.client.get(self.url, {'date': self.test_data['date']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        entry = response.data[0]
        self.assertEqual(entry['food_name'], self.test_data['food_name'])
        self.assertEqual(entry['total_calories'], self.test_data['total_calories'])
        self.assertEqual(entry['total_protein'], self.test_data['total_protein'])
        self.assertEqual(entry['total_fats'], self.test_data['total_fats'])
        self.assertEqual(entry['total_carbs'], self.test_data['total_carbs'])
        self.assertEqual(entry['food_weight'], self.test_data['food_weight'])

    def test_get_food_entries_by_date_no_date(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Date parameter is required.')

    def test_get_food_entries_by_date_not_found(self):
        response = self.client.get(self.url, {'date': '2024-09-02'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No entries found for the given date.')

    def test_post_food_entry(self):
        new_entry = {
            'food_name': 'New Food',
            'total_calories': 600,
            'total_protein': 40,
            'total_fats': 25,
            'total_carbs': 60,
            'food_weight': 250
        }
        response = self.client.post(self.url, data=json.dumps(new_entry), content_type=self.content_type, QUERY_STRING=f"date={self.test_data['date']}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['food_name'], 'New Food')

    def test_post_food_entry_no_date(self):
        new_entry = {
            'food_name': 'New Food',
            'total_calories': 600,
            'total_protein': 40,
            'total_fats': 25,
            'total_carbs': 60,
            'food_weight': 250
        }
        response = self.client.post(self.url, data=json.dumps(new_entry), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Date parameter is required.')

    def test_patch_food_entry(self):
        updated_entry = {
            'total_calories': 700,
            'total_protein': 50
        }
        response = self.client.patch(self.url, data=json.dumps(updated_entry), content_type=self.content_type, QUERY_STRING='id={}'.format(self.food_entry.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_calories'], 700)
        self.assertEqual(response.data['total_protein'], 50)

    def test_patch_food_entry_no_id(self):
        updated_entry = {
            'total_calories': 700,
            'total_protein': 50
        }
        response = self.client.patch(self.url, data=json.dumps(updated_entry), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Entry ID is required.')

    def test_patch_food_entry_not_found(self):
        updated_entry = {
            'total_calories': 700,
            'total_protein': 50
        }
        response = self.client.patch(self.url, data=json.dumps(updated_entry), content_type=self.content_type, QUERY_STRING='id=999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Entry not found.')

    def test_delete_food_entry(self):
        response = self.client.delete(self.url, QUERY_STRING='id={}'.format(self.food_entry.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_food_entry_no_id(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Entry ID is required.')

    def test_delete_food_entry_not_found(self):
        response = self.client.delete(self.url, QUERY_STRING='id=999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Entry not found.')

    def test_delete_food_entry_with_another_users_id(self):
        another_user = User.objects.create(id=2, username="Hacker")
        self.client.force_authenticate(user=another_user)

        test_user_row = FoodEntryTracking.objects.all()[0].id

        response = self.client.delete(self.url, QUERY_STRING=f'id={ test_user_row }')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Entry not found.')
