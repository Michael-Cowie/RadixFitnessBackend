import json
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Weights


class WeightsTest(TestCase):

    def date_as_datetime(self, date):
        return datetime.strptime(date, '%Y-%m-%d').date()

    def setUp(self):
        self.content_type = 'application/json'
        self.user = User.objects.get(id=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(id=1, username='Test User')

        def _create_weight_tracking_entry(date, weight):
            return Weights.objects.create(
                date=date,
                weight_kg=weight,
                user_id=user
            )

        _create_weight_tracking_entry('2024-01-01', 70)
        _create_weight_tracking_entry('2024-01-08', 71)
        _create_weight_tracking_entry('2024-01-13', 72)
        _create_weight_tracking_entry('2024-01-20', 73)
        _create_weight_tracking_entry('2024-01-27', 74)
        _create_weight_tracking_entry('2024-02-01', 163)
        _create_weight_tracking_entry('2024-02-08', 167.5)
        _create_weight_tracking_entry('2024-02-15', 171.33)


class AllWeightsView(WeightsTest):

    def setUp(self):
        super().setUp()
        self.test_url = reverse('all_weights')
        self.data = self.client.get(self.test_url).data

    def test_correct_response_data(self):
        """
        Verify that the View has returned the correct data for the test user.
        """
        for weight in self.data:
            expected_weight = Weights.objects.get(id=weight['id'])
            self.assertEqual(self.date_as_datetime(weight['date']), expected_weight.date)
            self.assertEqual(weight['weight_kg'], expected_weight.weight_kg)
            self.assertEqual(weight['user_id'], expected_weight.user_id.id)

    def test_correct_number_of_expected_users(self):
        """
        Verify that the response data is the expected length.
        """
        number_of_weights = Weights.objects.filter().count()
        number_of_response_weights = len(self.data)
        self.assertEqual(number_of_weights, number_of_response_weights)

    def test_request_for_empty_user(self):
        """
        Verify that the View correctly handles a user with no weight entries.
        """
        new_user = User.objects.create(id=2, username='new user username')
        self.client.force_authenticate(user=new_user)

        data = self.client.get(self.test_url).data
        self.assertEqual(len(data), 0)

    def test_dates_return_in_descending_order(self):
        """
        Verify that the weights are returned in descending order where the most recent date will be at index 0.
        """
        new_user = User.objects.create(id=2, username='new user username')
        self.client.force_authenticate(user=new_user)

        def _create_weight_tracking_entry(date, weight):
            return Weights.objects.create(
                date=date,
                weight_kg=weight,
                user_id=new_user
            )

        expected_list = [
            '2024-12-25',
            '2024-12-20',
            '2024-09-17',
            '2024-08-16',
            '2024-05-01',
            '2024-01-02',
            '2024-01-01',
            '2023-12-25',
            '2023-05-18',
        ]

        for position in [8, 3, 2, 7,  0, 4, 1, 5, 6]:  # Add to database in a random order.
            _create_weight_tracking_entry(expected_list[position], 50 + position)

        returned_data = self.client.get(self.test_url).data

        for expected_position in range(len(returned_data)):
            self.assertEqual(returned_data[expected_position]['date'], expected_list[expected_position])


class WeightsViewTest(WeightsTest):

    def setUp(self):
        super().setUp()
        self.test_url = reverse('weights')

        self.date = '2000-01-01'
        self.weight = 200.00
        self.data = json.dumps({
            'date': self.date,
            'weight_kg': self.weight
        })

    def test_creating_a_weight(self):
        # 1. Send a POST to create the weight
        response = self.client.post(self.test_url, data=self.data, content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        response_id = response_data['id']

        # 2. Validate it was populated in the model with the correct data inside the http body
        created_weight = Weights.objects.get(id=response_id)

        self.assertEqual(self.date_as_datetime(self.date), created_weight.date)
        self.assertEqual(self.weight, created_weight.weight_kg)
        self.assertEqual(self.user, created_weight.user_id)

    def test_creating_two_weights_same_day(self):
        # 1. Send a POST to create the weight
        self.client.post(self.test_url, data=self.data, content_type=self.content_type)

        # 2. Send a POST to create a same on the same day
        response = self.client.post(self.test_url, data=self.data, content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_a_weight(self):
        # 1. Send a POST to create the weight
        self.client.post(self.test_url, data=self.data, content_type=self.content_type)

        # 2. Send a PATCH to update the weight and unit
        new_weight = 230
        new_data = json.dumps({
            'date': self.date,
            'weight_kg': new_weight
        })
        response = self.client.patch(self.test_url, data=new_data, content_type=self.content_type)

        # 3. Verify that the weight has been updated in the model
        weight_id = response.data['id']
        model_weight = Weights.objects.get(id=weight_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_weight, int(model_weight.weight_kg))

    def test_partially_updating_a_weight(self):
        # 1. Send a POST to create the weight
        self.client.post(self.test_url, data=self.data, content_type=self.content_type)

        # 2. Send a PATCH to update only the weight
        new_weight = 999
        new_data = json.dumps({
            'date': self.date,
            'weight_kg': new_weight
        })

        response = self.client.patch(self.test_url, data=new_data, content_type=self.content_type)

        # 3. Verify that the weight has been updated in the model and the unit remains unchanged
        weight_id = response.data['id']
        model_weight = Weights.objects.get(id=weight_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_weight, int(model_weight.weight_kg))

    def test_updating_notes(self):
        # 1. Send a POST to create the weight
        data = json.dumps({
            'date': self.date,
            'weight_kg': self.weight,
            'notes': 'My initial notes'
        })

        self.client.post(self.test_url, data=data, content_type=self.content_type)

        # 2. Send a PATCH to update only the notes
        new_notes = "My new notes"
        new_data = json.dumps({
            'date': self.date,
            'notes': new_notes
        })

        response = self.client.patch(self.test_url, data=new_data, content_type=self.content_type)

        # 3. Verify that the notes has been updated in the model and the unit remains unchanged
        weight_id = response.data['id']
        model_weight = Weights.objects.get(id=weight_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_notes, model_weight.notes)

    def test_deleting_a_weight(self):
        # 1. Send a POST to create the weight
        response = self.client.post(self.test_url, data=self.data, content_type=self.content_type)
        weight_id = response.data['id']

        # 2. Send a DELETE to delete the weight
        response = self.client.delete(self.test_url, data=self.data, content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 5. Verify that the weight has been deleted.
        with self.assertRaises(Weights.DoesNotExist):
            Weights.objects.get(id=weight_id)

