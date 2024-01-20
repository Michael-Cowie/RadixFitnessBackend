import json
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Units, Weights


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

        def _create_weight_tracking_entry(date, weight, unit):
            return Weights.objects.create(
                date=date,
                weight=weight,
                unit=unit,
                user_id=user
            )

        _create_weight_tracking_entry('2024-01-01', 70, Units.KILOGRAM)
        _create_weight_tracking_entry('2024-01-08', 71, Units.KILOGRAM)
        _create_weight_tracking_entry('2024-01-13', 72, Units.KILOGRAM)
        _create_weight_tracking_entry('2024-01-20', 73, Units.KILOGRAM)
        _create_weight_tracking_entry('2024-01-27', 74, Units.KILOGRAM)
        _create_weight_tracking_entry('2024-02-01', 163, Units.POUND)
        _create_weight_tracking_entry('2024-02-08', 167.5, Units.POUND)
        _create_weight_tracking_entry('2024-02-15', 171.33, Units.POUND)


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
            self.assertEqual(weight['weight'], str(expected_weight.weight))
            self.assertEqual(weight['unit'], expected_weight.unit)
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


class WeightsViewTest(WeightsTest):

    def setUp(self):
        super().setUp()
        self.test_url = reverse('weights')

        self.date = '2000-01-01'
        self.weight = '200.00'
        self.unit = 'kg'
        self.data = json.dumps({
            'date': self.date,
            'weight': self.weight,
            'unit': self.unit
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
        self.assertEqual(self.weight, str(created_weight.weight))
        self.assertEqual(self.unit, created_weight.unit)
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
        new_weight = 200
        new_unit = 'lbs'
        new_data = json.dumps({
            'date': self.date,
            'weight': new_weight,
            'unit': new_unit
        })
        response = self.client.patch(self.test_url, data=new_data, content_type=self.content_type)

        # 3. Verify that the weight has been updated in the model
        weight_id = response.data['id']
        model_weight = Weights.objects.get(id=weight_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_weight, int(model_weight.weight))
        self.assertEqual(new_unit, model_weight.unit)

    def test_partially_updating_a_weight(self):
        # 1. Send a POST to create the weight
        self.client.post(self.test_url, data=self.data, content_type=self.content_type)

        # 2. Send a PATCH to update only the weight
        new_weight = 200
        new_data = json.dumps({
            'date': self.date,
            'weight': new_weight
        })

        response = self.client.patch(self.test_url, data=new_data, content_type=self.content_type)

        # 3. Verify that the weight has been updated in the model and the unit remains unchanged
        weight_id = response.data['id']
        model_weight = Weights.objects.get(id=weight_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_weight, int(model_weight.weight))
        self.assertEqual(self.unit, model_weight.unit)

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
