from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Profile


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username='Test User')

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_create_basic_profile(self):
        name = "Michael"
        measurement_system = "Metric"

        profile = Profile.objects.create(
            name=name,
            measurement_system=measurement_system,
            user_id=self.user
        )
        profile.full_clean()

        self.assertEqual(profile.name, name)
        self.assertEqual(profile.measurement_system, measurement_system)
        self.assertEqual(profile.user_id, self.user)

    def test_incorrect_name_type(self):
        name = "Invalid 123"
        with self.assertRaises(ValidationError):
            profile = Profile.objects.create(
                name=name,
                user_id=self.user
            )
            profile.full_clean()

    def test_incorrect_name_length(self):
        name = ''
        with self.assertRaises(ValidationError):
            profile = Profile.objects.create(
                name=name,
                user_id=self.user
            )
            profile.full_clean()
