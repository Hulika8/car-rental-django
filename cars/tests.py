from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Car


class CarModelTests(TestCase):
    def test_can_be_rented_true(self):
        car = Car.objects.create(
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
        self.assertTrue(car.can_be_rented())

    def test_can_be_rented_false_when_damaged(self):
        car = Car.objects.create(
            brand="Toyota",
            model="Corolla",
            year=2020,
            color="White",
            daily_rate=Decimal("100.00"),
            in_fleet=True,
            is_rented=False,
            is_damaged=True,
            is_maintenance=False,
        )
        self.assertFalse(car.can_be_rented())

    def test_get_rental_status_available(self):
        car = Car.objects.create(
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
        self.assertEqual(car.get_rental_status(), "Available for Rental")

    def test_daily_rate_validation(self):
        car = Car(
            brand="Toyota",
            model="Corolla",
            year=2020,
            color="White",
            daily_rate=Decimal("0.00"),
            in_fleet=True,
            is_rented=False,
            is_damaged=False,
            is_maintenance=False,
        )
        with self.assertRaises(ValidationError):
            car.clean() # Validation only: we call clean() directly (no save) to check if the conditions in the model are met.