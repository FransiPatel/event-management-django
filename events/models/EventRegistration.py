import uuid
from django.db import models
import time
from users.models import User
from .Event import Event


class EventRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    userId = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="registrations"
    )
    eventId = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
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
        db_table = "event_registration"
