import uuid
from django.db import models
from .Media import Media
from users.models import User
import time


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()

    datetime = models.DateTimeField()  # event date & time

    venue = models.CharField(max_length=255)  # location/venue name
    capacity = models.PositiveIntegerField()

    userId = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        db_column="userId",
    )

    imageId = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        db_column="imageId",
    )
    # Unix timestamp fields
    createdAt = models.BigIntegerField(default=int(time.time() * 1000))
    updatedAt = models.BigIntegerField(null=True)
    deletedAt = models.BigIntegerField(null=True)

    # User fields
    createdBy = models.CharField(
        max_length=255,
        null=True,
    )
    updatedBy = models.CharField(
        max_length=255,
        null=True,
    )
    deletedBy = models.CharField(
        max_length=255,
        null=True,
    )
    isDeleted = models.BooleanField(default=False)

    class Meta:
        db_table = "event"

    def __str__(self):
        return self.title
