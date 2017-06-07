from datetime import date, timedelta

from django.test import TestCase

from ..factories import ReservationFactory, UserFactory, TEST_PASSWORD


class ReservationApiGetListTestCase(TestCase):
    def test_should_return_403_for_non_authenticated_user(self):
        response = self.client.get('/api/v1/reservations/')
        self.assertEqual(response.status_code, 403)

    def test_should_return_list_of_reservations_for_authenticated_user(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)

        for _ in range(3):
            ReservationFactory(creator=user)

        response = self.client.get('/api/v1/reservations/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(data['count'], 3)

    def test_should_allow_search_by_date_range(self):
        user = UserFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)

        ReservationFactory(
            creator=user,
            start_date=date.today() - timedelta(days=5),
            end_date = date.today() - timedelta(days=2),
        )
        ReservationFactory(
            creator=user,
            start_date=date.today() + timedelta(days=2),
            end_date = date.today() + timedelta(days=5),
        )
        current_res = ReservationFactory(
            creator=user,
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
