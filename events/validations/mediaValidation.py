from rest_framework import serializers
from event_management.constants import (
    USER_MEDIA_UPLOAD_TYPE,
)


# Validate upload media request data
class UploadMediaRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    typeOfFile = serializers.CharField(required=True)
    duration = serializers.IntegerField(required=False, default=0, min_value=0)
    eventCode = serializers.CharField(required=False, allow_blank=True)

    # Check for the allowed upload types (video, image)
    def validate_typeOfFile(self, value):
        if value not in list(USER_MEDIA_UPLOAD_TYPE.values()):
            raise serializers.ValidationError("Invalid upload type")

        return value


class FileUploadValidator:

    @staticmethod
    def validate(upload_type, file):
        if not file:
            raise serializers.ValidationError("File is required.")

        file_type = file.content_type.split("/")[-1].lower()
        file_size = file.size

        # Determine allowed types + max size
        if upload_type in [
            USER_MEDIA_UPLOAD_TYPE["EventCoverImage"],
        ]:
            max_size = 5 * 1024 * 1024  # 5MB
            allowed = ["jpeg", "jpg", "png", "gif"]

        else:
            raise serializers.ValidationError("Invalid uploadType")

        # Validate size
        if file_size > max_size:
            raise serializers.ValidationError("File too large")

        # Validate file extension
        if file_type not in allowed:
            raise serializers.ValidationError("Invalid file type")

        return True
