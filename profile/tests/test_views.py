import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Profile


class ProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username='Test User')

    def setUp(self):
        self.user = User.objects.get(id=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.content_type = 'application/json'
        self.test_url = reverse('profile')

        self.data_name = "Michael"
        self.data = json.dumps({
            "name": self.data_name
        })

    def test_create_profile(self):
        # 1. Send a POST to create the profile
        response = self.client.post(self.test_url, data=self.data, content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        profile_id = response.data['id']

        # 2. Validate it was populated in the model with the correct data inside the http body
        created_profile = Profile.objects.get(id=profile_id)
        self.assertEqual(created_profile.name, self.data_name)
        self.assertEqual(created_profile.user_id, self.user)

    def test_creation_error_throws_error(self):
        # 1. Send a POST to create the profile with incorrect data
        self.data = json.dumps({
            "name": "Invalid 123"
        })
        response = self.client.post(self.test_url, data=self.data, content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile(self):
        # 1. Create out test profile, that we will late fetch
        test_name = "Michael"
        Profile.objects.create(
            name=test_name,
            user_id=self.user
        )

        # 2. Send a GET and attempt to fetch the user profile
        response = self.client.get(self.test_url)
        self.assertEqual(response.data['name'], test_name)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_update_profile(self):
        # 1. Create out test profile
        test_name = "Michael"
        profile = Profile.objects.create(
            name=test_name,
            user_id=self.user
        )
        self.assertEqual(profile.name, test_name)

        # 2. Send a POST to update the user profile and validate that it has updated
        new_name = "UpdatedName"
        data = json.dumps({
            "name": new_name
        })
        response = self.client.patch(self.test_url, data=data, content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile_id = response.data['id']

        updated_profile = Profile.objects.get(id=profile_id)
        self.assertEqual(updated_profile.name, new_name)

    def test_deleting_profile(self):
        # 1. Create out test profile
        test_name = "Michael"
        Profile.objects.create(
            name=test_name,
            user_id=self.user
        )
        self.assertEqual(Profile.objects.filter().count(), 1)

        # 2. Send a DELETE to delete our profile and validate it's removed from the model
        response = self.client.delete(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Profile.objects.filter().count(), 0)
