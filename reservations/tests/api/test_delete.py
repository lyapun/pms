from datetime import date, timedelta

from rest_framework.test import APITestCase

from reservations.models import Reservation

from ..factories import UserFactory, TEST_PASSWORD, ReservationFactory


class ReservationApiDeleteTestCase(APITestCase):
    def test_should_return_403_for_non_auth_user(self):
        response = self.client.delete('/api/v1/reservations/')
        self.assertEqual(response.status_code, 403)

    def test_should_return_404_for_non_existed_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.delete('/api/v1/reservations/777/')
        self.assertEqual(response.status_code, 404)

    def test_should_return_403_if_try_to_delete_non_own_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory()
        response = self.client.delete('/api/v1/reservations/{}/'.format(
            reservation.id
        ))
        self.assertEqual(response.status_code, 403)

    def test_should_delete_own_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(creator=user)
        response = self.client.delete('/api/v1/reservations/{}/'.format(
            reservation.id
        ))
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(
            Reservation.objects.filter(id=reservation.id).first()
        )
        self.assertTrue(Reservation.all_objects.get(id=reservation.id).deleted)
