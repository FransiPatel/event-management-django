from rest_framework import serializers
from ..models.Media import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "mediaUrl",
            "mediaName",
            "type",
            "duration",
            "isExternal",
            "source",
            "createdAt",
            "updatedAt",
            "deletedAt",
            "createdBy",
            "updatedBy",
            "deletedBy",
            "isDeleted",
        ]
        read_only_fields = ["id"]
