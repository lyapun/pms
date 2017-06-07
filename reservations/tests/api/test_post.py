from datetime import date, timedelta

from rest_framework.test import APITestCase

from reservations.models import Reservation

from ..factories import UserFactory, TEST_PASSWORD


class ReservationApiPostTestCase(APITestCase):
    def test_should_return_403_for_non_auth_user(self):
        response = self.client.post('/api/v1/reservations/')
        self.assertEqual(response.status_code, 403)

    def test_should_create_reservation_for_valid_data_for_auth_user(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        start_date = date.today()
        end_date = date.today() + timedelta(days=1)
        data = {
            'start_date': str(start_date),
            'end_date': str(end_date),
            'room_number': 1,
            'first_name': 'Test',
            'last_name': 'Test'
        }
        response = self.client.post(
            '/api/v1/reservations/', data=data, format='json',
        )
        self.assertEqual(response.status_code, 201)
        reservation = Reservation.objects.get(id=response.json()['id'])
        self.assertEqual(reservation.creator, user)
        self.assertEqual(reservation.start_date, start_date)
        self.assertEqual(reservation.end_date, end_date)
        self.assertEqual(reservation.room_number, 1)
        self.assertEqual(reservation.first_name, 'Test')
        self.assertEqual(reservation.last_name, 'Test')

    def test_should_require_all_fields_to_create_reservation(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.post(
            '/api/v1/reservations/', data={}, format='json',
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        for key in ('start_date', 'end_date', 'room_number', 'first_name',
                    'last_name'):
            self.assertTrue(key in data)
