from django.contrib.auth.models import User
from django.test import TestCase

from .models import UserProfile


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass1234",
            first_name="Test",
            last_name="User",
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone="5550001111",
            address="Main St 1",
            city="Istanbul",
            state="TR",
            zip_code="34000",
            license_number="LIC-123",
            date_of_birth="1990-01-01",
            is_verified=True,
            is_active=True,
        )

    def test_can_make_reservations_true(self):
        self.assertTrue(self.profile.can_make_reservations())

    def test_can_make_reservations_false_when_not_verified(self):
        self.profile.is_verified = False
        self.profile.save()
        self.assertFalse(self.profile.can_make_reservations())

    def test_get_full_name(self):
        self.assertEqual(self.profile.get_full_name(), "Test User")

    def test_get_full_address(self):
        self.assertEqual(
            self.profile.get_full_address(),
            "Main St 1, Istanbul, TR, 34000"
        )