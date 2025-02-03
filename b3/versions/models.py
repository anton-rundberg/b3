from django.db import models

from utils.models import TimestampedModel, UUIDModel


class Version(UUIDModel, TimestampedModel):
    minimum_version = models.CharField(max_length=256)

    def __str__(self):
        return f"Minimum version: {self.minimum_version}"
