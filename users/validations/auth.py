from rest_framework import serializers
from django.contrib.auth import get_user_model
from event_management.responseMessage import *
import re
from event_management.constants import PASSWORD_REGEX

User = get_user_model()


class RegisterValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_EXISTS)
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(USERNAME_ALREADY_EXISTS)
        return value

    def validate_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError(
                "Password must be 8-15 characters long and contain only valid special characters."
            )
        return value


class RegisterSocialValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    googleId = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_EXISTS)
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(USERNAME_ALREADY_EXISTS)
        return value

    def validate_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError(
                "Password must be 8-15 characters long and contain only valid special characters."
            )
        return value


class LoginValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CreateAdminValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_EXISTS)
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(USERNAME_ALREADY_EXISTS)
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        if not re.search(r"[!@#$%^&*]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )
        return value
