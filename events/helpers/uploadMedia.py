import os
import time
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils.crypto import get_random_string
from ..serializers import MediaSerializer
from event_management.responseMessage import *


def uploadMedia(user, file):
    upload_dir = "uploads"
    timestamp = int(time.time() * 1000)
    unique_filename = f"{timestamp}_{get_random_string(6)}_{file.name}"
    file_path = os.path.join(upload_dir, unique_filename)

    saved_path = default_storage.save(file_path, file)

    # Try to obtain a publicly accessible URL for the saved file.
    try:
        media_url = default_storage.url(saved_path)
    except Exception:
        media_url = f"{settings.MEDIA_URL}{unique_filename}"

    file_type = getattr(file, "content_type", "application/octet-stream")

    media_data = {
        "mediaUrl": media_url,
        "mediaName": file.name,
        "type": file_type,
        "isExternal": False,
        "source": "upload",
        "createdBy": str(user.id),
    }

    serializer = MediaSerializer(data=media_data)
    if serializer.is_valid():
        serializer.save()
        return {"ok": True, "data": serializer.data, "path": saved_path}

    # cleanup saved file on serializer failure
    try:
        default_storage.delete(saved_path)
    except Exception:
        pass

    return {"ok": False, "errors": serializer.errors, "path": None}
