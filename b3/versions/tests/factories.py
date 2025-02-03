import factory

from .. import models


class VersionFactory(factory.django.DjangoModelFactory):
    minimum_version = factory.Sequence(lambda n: f"1.0.{n}")

    class Meta:
        model = models.Version
