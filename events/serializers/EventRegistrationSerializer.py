from rest_framework import serializers
from ..models.EventRegistration import EventRegistration


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = [
            "id",
            "userId",
            "eventId",
            "createdAt",
            "updatedAt",
            "deletedAt",
            "createdBy",
            "updatedBy",
            "deletedBy",
            "isDeleted",
        ]
        read_only_fields = ["id"]
