import json
from profile.models import Profile

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.test_url = reverse("profile")
        self.content_type = "application/json"
        self.default_data = {
            "name": "Michael",
            "measurement_system": "Metric",
        }

    def test_create_profile_success(self):
        response = self.client.post(
            self.test_url,
            data=json.dumps(self.default_data),
            content_type=self.content_type,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.name, self.default_data["name"])
        self.assertEqual(profile.measurement_system, self.default_data["measurement_system"])

    def test_create_profile_invalid_data_returns_400(self):
        invalid_data = {"name": "Invalid 123"}
        response = self.client.post(
            self.test_url,
            data=json.dumps(invalid_data),
            content_type=self.content_type,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_returns_correct_data(self):
        Profile.objects.create(
            name=self.default_data["name"],
            measurement_system=self.default_data["measurement_system"],
            user=self.user,
        )
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.default_data["name"])
        self.assertEqual(response.data["user"], self.user.id)

    def test_update_profile_name(self):
        Profile.objects.create(
            name=self.default_data["name"],
            measurement_system=self.default_data["measurement_system"],
            user=self.user,
        )
        new_name = "UpdatedName"
        response = self.client.patch(
            self.test_url,
            data=json.dumps({"name": new_name}),
            content_type=self.content_type,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.name, new_name)

    def test_partial_update_profile_measurement_system(self):
        Profile.objects.create(
            name=self.default_data["name"],
            measurement_system=self.default_data["measurement_system"],
            user=self.user,
        )
        new_system = "Imperial"
        response = self.client.patch(
            self.test_url,
            data=json.dumps({"measurement_system": new_system}),
            content_type=self.content_type,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.measurement_system, new_system)

    def test_delete_profile_removes_instance(self):
        Profile.objects.create(
            name=self.default_data["name"],
            measurement_system=self.default_data["measurement_system"],
            user=self.user,
        )
        self.assertEqual(Profile.objects.count(), 1)

        response = self.client.delete(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profile.objects.count(), 0)
