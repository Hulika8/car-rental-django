from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from cars.models import Car
from users.models import UserProfile
from .models import Reservation


class ReservationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass1234",
            first_name="Test",
            last_name="User",
        )
        UserProfile.objects.create(
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

        self.car = Car.objects.create(
            brand="Toyota",
            model="Corolla",
            year=2020,
            color="White",
            daily_rate=Decimal("100.00"),
            in_fleet=True,
            is_rented=False,
            is_damaged=False,
            is_maintenance=False,
        )

    def _create_reservation(self, start_days=3, duration_days=2, status="pending"):
        start_date = (timezone.now() + timedelta(days=start_days)).date()
        end_date = start_date + timedelta(days=duration_days)
        return Reservation.objects.create(
            user=self.user,
            car=self.car,
            start_date=start_date,
            end_date=end_date,
            daily_rate=Decimal("100.00"),
            status=status,
        )

    def test_get_total_amount(self):
        reservation = self._create_reservation(duration_days=3)
        self.assertEqual(reservation.get_total_amount(), Decimal("300.00"))

    def test_can_be_cancelled_status(self):
        pending = self._create_reservation(start_days=3, status="pending")
        confirmed = self._create_reservation(start_days=6, status="confirmed")
        active = self._create_reservation(start_days=9, status="active")

        self.assertTrue(pending.can_be_cancelled())
        self.assertTrue(confirmed.can_be_cancelled())
        self.assertFalse(active.can_be_cancelled())

    def test_cancellation_fee_more_than_48_hours(self):
        reservation = self._create_reservation(start_days=3, duration_days=2, status="pending")
        self.assertEqual(reservation.get_cancellation_fee(), Decimal("0.00"))

    def test_cancellation_fee_between_24_and_48_hours(self):
        reservation = self._create_reservation(start_days=2, duration_days=2, status="pending")
        self.assertEqual(reservation.get_cancellation_fee(), Decimal("100.00"))

    def test_cancellation_fee_less_than_24_hours(self):
        reservation = self._create_reservation(start_days=1, duration_days=2, status="pending")
        self.assertEqual(reservation.get_cancellation_fee(), Decimal("200.00"))

    def test_cancellation_fee_invalid_status(self):
        reservation = self._create_reservation(status="active")
        self.assertIsNone(reservation.get_cancellation_fee())