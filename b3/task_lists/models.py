from django.db import models

from utils.models import TimestampedModel, UUIDModel


class List(UUIDModel, TimestampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Task(UUIDModel, TimestampedModel):
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
