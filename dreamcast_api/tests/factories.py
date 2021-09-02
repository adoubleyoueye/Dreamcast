from datetime import timedelta, timezone
from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from dreamcast_api.models import Wants

faker = Factory.create()


class WantsFactory(DjangoModelFactory):
    class Meta:
        model = Wants

    want = LazyAttribute(lambda o: faker.text(max_nb_chars=1000))
    manifested_on = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())
