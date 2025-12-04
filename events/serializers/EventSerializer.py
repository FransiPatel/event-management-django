from rest_framework import serializers
from ..models.Event import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "datetime",
            "venue",
            "capacity",
            "imageId",
            "createdBy",
            "updatedBy",
            "deletedBy",
            "createdAt",
            "updatedAt",
            "deletedAt",
        ]
        read_only_fields = [
            "id",
        ]
