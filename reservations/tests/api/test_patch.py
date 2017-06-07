from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from ..factories import UserFactory, TEST_PASSWORD, ReservationFactory


class ReservationApiPatchTestCase(APITestCase):
    def test_should_return_403_for_non_auth_user(self):
        response = self.client.patch('/api/v1/reservations/')
        self.assertEqual(response.status_code, 403)

    def test_should_return_404_for_non_existed_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.patch('/api/v1/reservations/777/')
        self.assertEqual(response.status_code, 404)

    def test_should_return_403_if_try_to_delete_not_own_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory()
        response = self.client.patch('/api/v1/reservations/{}/'.format(
            reservation.id
        ))
        self.assertEqual(response.status_code, 403)

    def test_should_update_own_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(creator=user)
        data = {'first_name': 'new first name'}
        response = self.client.patch('/api/v1/reservations/{}/'.format(
            reservation.id
        ), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        reservation.refresh_from_db()
        self.assertEqual(reservation.first_name, 'new first name')

    def test_is_not_possible_to_change_creator(self):
        user = UserFactory()
        other_user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(creator=user)
        data = {'creator': other_user.id}
        self.client.patch('/api/v1/reservations/{}/'.format(
            reservation.id
        ), data=data, format='json')
        reservation.refresh_from_db()
        self.assertEqual(reservation.creator, user)

    def test_is_not_possible_to_change_created_at(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(creator=user)
        old_created_at = reservation.created_at
        data = {'created_at': (datetime.now() - timedelta(days=1)).isoformat()}
        self.client.patch('/api/v1/reservations/{}/'.format(
            reservation.id
        ), data=data, format='json')
        reservation.refresh_from_db()
        self.assertEqual(reservation.created_at, old_created_at)

    def test_is_not_possible_to_change_updated_at(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(creator=user)
        old_updated_at = reservation.updated_at
        data = {'updated_at': (datetime.now() - timedelta(days=1)).isoformat()}
        self.client.patch('/api/v1/reservations/{}/'.format(
            reservation.id
        ), data=data, format='json')
        reservation.refresh_from_db()
        self.assertTrue(reservation.updated_at > old_updated_at)
