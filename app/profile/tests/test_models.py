from profile.models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")

    def test_profile_creation_with_valid_data(self):
        profile = Profile.objects.create(
            name="Michael",
            measurement_system="Metric",
            user=self.user,
        )
        profile.full_clean()
        self.assertEqual(profile.name, "Michael")
        self.assertEqual(profile.measurement_system, "Metric")
        self.assertEqual(profile.user, self.user)

    def test_validation_fails_for_name_with_invalid_characters(self):
        profile = Profile(name="Invalid 123", user=self.user)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_validation_fails_for_empty_name(self):
        profile = Profile(name="", user=self.user)
        with self.assertRaises(ValidationError):
            profile.full_clean()
