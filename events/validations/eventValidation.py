from rest_framework import serializers
from event_management.responseMessage import *


class CreateEventValidator(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    datetime = serializers.DateTimeField(required=True)
    venue = serializers.CharField(required=True)
    capacity = serializers.IntegerField(required=True)
    imageId = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_capacity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError(INVALID_CAPACITY)
        return value


class UpdateEventValidator(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    datetime = serializers.DateTimeField(required=False)
    venue = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    capacity = serializers.IntegerField(required=False)
    imageId = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    deletedMediaId = serializers.CharField(
        required=False, allow_null=True, allow_blank=False
    )

    def validate_capacity(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(INVALID_CAPACITY)
        return value


class DeleteEventValidator(serializers.Serializer):
    id = serializers.CharField(required=True)


class RegisterEventValidator(serializers.Serializer):
    eventId = serializers.CharField(required=True)
