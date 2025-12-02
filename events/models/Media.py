import uuid
from django.db import models
import time


class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Unix timestamp fields
    createdAt = models.BigIntegerField(default=int(time.time() * 1000))
    updatedAt = models.BigIntegerField(null=True)
    deletedAt = models.BigIntegerField(null=True)

    # Additional fields
    mediaUrl = models.CharField(max_length=500, null=True, blank=True)
    mediaName = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    duration = models.FloatField(default=0)

    isExternal = models.BooleanField(default=False)

    source = models.CharField(max_length=255, null=True, blank=True)

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
        db_table = "media"

    def __str__(self):
        return self.mediaName or str(self.id)
