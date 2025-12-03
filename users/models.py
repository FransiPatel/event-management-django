import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import time
from event_management.constants import USER_PROFILE_TYPE


class UserManager(BaseUserManager):
    def create_user(self, username, email, firstName, lastName, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


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
    profileType = models.CharField(
        max_length=255, null=True, blank=False, default=USER_PROFILE_TYPE["User"]
    )
    isDeleted = models.BooleanField(default=False)

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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "firstName", "lastName"]

    class Meta:
        db_table = "user"
