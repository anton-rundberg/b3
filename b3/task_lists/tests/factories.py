import factory

from .. import models


class ListFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("users.tests.factories.UserFactory")

    class Meta:
        model = models.List


class TaskFactory(factory.django.DjangoModelFactory):
    list = factory.SubFactory(ListFactory)

    name = factory.Faker("first_name")

    class Meta:
        model = models.Task
