from datetime import date, timedelta

import factory

from django.conf import settings

TEST_PASSWORD = 'test1234'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username', )

    username = factory.Sequence(lambda n: 'user-{}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'reservations.Reservation'

    room_number = factory.Sequence(int)
    start_date = factory.LazyFunction(date.today)
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=1))
    first_name = factory.Sequence(lambda n: 'first-{}'.format(n))
    last_name = factory.Sequence(lambda n: 'last-{}'.format(n))
    creator = factory.SubFactory(UserFactory)
