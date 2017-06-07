from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from reservations.models import Reservation

from .factories import UserFactory, ReservationFactory


class ReservationTestCase(TestCase):
    def test_model_creation(self):
        reservation = Reservation.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            first_name='Test',
            last_name='Test',
            room_number=1,
            creator=UserFactory(),
        )
        self.assertIsNotNone(reservation.id)

    def test_should_not_allow_same_room_same_dates(self):
        ReservationFactory(
            room_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                start_date=date.today(),
                end_date=date.today() + timedelta(days=1),
                first_name='Test',
                last_name='Test',
                room_number=1,
                creator=UserFactory(),
            )

    def test_should_not_allow_room_dates_overlap_with_start_date(self):
        ReservationFactory(
            room_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
        )
        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
                first_name='Test',
                last_name='Test',
                room_number=1,
                creator=UserFactory(),
            )

    def test_should_not_allow_room_dates_inside_start_end_range(self):
        ReservationFactory(
            room_number=1,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
        )
        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                start_date=date.today(),
                end_date=date.today() + timedelta(days=1),
                first_name='Test',
                last_name='Test',
                room_number=1,
                creator=UserFactory(),
            )

    def test_should_not_allow_room_dates_overlap_with_end_date(self):
        ReservationFactory(
            room_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
        )
        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                start_date=date.today() + timedelta(days=1),
                end_date=date.today() + timedelta(days=4),
                first_name='Test',
                last_name='Test',
                room_number=1,
                creator=UserFactory(),
            )

    def test_model_delete_should_change_deleted_field(self):
        reservation = ReservationFactory()
        reservation.delete()
        reservation = Reservation.all_objects.get(id=reservation.id)
        self.assertTrue(reservation.deleted)

    def test_deleted_model_should_not_appear_in_query(self):
        reservation = ReservationFactory(deleted=True)
        self.assertIsNone(
            Reservation.objects.filter(id=reservation.id).first()
        )
