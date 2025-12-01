import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import time


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    # Auth fields
    token = models.TextField(null=True, blank=True)
    refreshToken = models.TextField(null=True, blank=True)
    socialId = models.CharField(max_length=255, null=True, blank=True)
    profileType = models.CharField(max_length=255, null=True, blank=False)
    isDeleted = models.BooleanField(default=False)

    # Unix timestamp fields
    createdAt = models.BigIntegerField(default=int(time.time() * 1000))
    updatedAt = models.BigIntegerField()
    deletedAt = models.BigIntegerField()

    # User fields
    createdBy = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    updatedBy = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    deletedBy = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "firstName", "lastName"]

    class Meta:
        db_table = "user"
