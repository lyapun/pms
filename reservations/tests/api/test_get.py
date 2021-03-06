from datetime import date, timedelta

from rest_framework.test import APITestCase

from ..factories import ReservationFactory, UserFactory, TEST_PASSWORD


class ReservationApiGetListTestCase(APITestCase):
    def test_should_return_403_for_non_authenticated_user(self):
        response = self.client.get('/api/v1/reservations/')
        self.assertEqual(response.status_code, 403)

    def test_should_return_list_of_reservations_for_authenticated_user(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)

        for _ in range(3):
            ReservationFactory()

        response = self.client.get('/api/v1/reservations/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(data['count'], 3)

    def test_should_allow_search_by_date_range(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)

        ReservationFactory(
            start_date=date.today() - timedelta(days=5),
            end_date = date.today() - timedelta(days=2),
        )
        ReservationFactory(
            start_date=date.today() + timedelta(days=2),
            end_date = date.today() + timedelta(days=5),
        )
        current_res = ReservationFactory(
            start_date=date.today() - timedelta(days=1),
            end_date = date.today() + timedelta(days=1),
        )

        response = self.client.get(
            '/api/v1/reservations/?start_date={}&end_date={}'.format(
                date.today(), date.today() + timedelta(days=1)
            )
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], current_res.id)

    def test_should_search_for_exact_dates(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )
        response = self.client.get(
            '/api/v1/reservations/?start_date={}&end_date={}'.format(
                date.today() - timedelta(days=1),
                date.today() + timedelta(days=1)
            )
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], reservation.id)

    def test_should_search_if_start_date_overlap(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
        )
        response = self.client.get(
            '/api/v1/reservations/?start_date={}&end_date={}'.format(
                date.today() - timedelta(days=1),
                date.today() + timedelta(days=1)
            )
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], reservation.id)

    def test_should_search_if_inside_start_end_range(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
        )
        response = self.client.get(
            '/api/v1/reservations/?start_date={}&end_date={}'.format(
                date.today(),
                date.today() + timedelta(days=1)
            )
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], reservation.id)

    def test_search_if_end_date_overlap(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        reservation = ReservationFactory(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
        )
        response = self.client.get(
            '/api/v1/reservations/?start_date={}&end_date={}'.format(
                date.today() + timedelta(days=1),
                date.today() + timedelta(days=4),
            )
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['id'], reservation.id)


class ReservationApiGetDetailsTestCase(APITestCase):
    def test_should_return_403_for_non_authenticated_user(self):
        response = self.client.get('/api/v1/reservations/1/')
        self.assertEqual(response.status_code, 403)

    def test_should_return_404_for_non_existed_object(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.get('/api/v1/reservations/777/')
        self.assertEqual(response.status_code, 404)

    def test_should_return_403_for_auth_user_if_not_creator(self):
        user = UserFactory()
        reservation = ReservationFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.get('/api/v1/reservations/{}/'.format(
            reservation.id
        ))
        self.assertEqual(response.status_code, 403)

    def test_should_return_200_for_auth_user_if_creator(self):
        user = UserFactory()
        reservation = ReservationFactory(creator=user)
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.get('/api/v1/reservations/{}/'.format(
            reservation.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], reservation.id)
