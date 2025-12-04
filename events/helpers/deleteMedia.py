from django.core.files.storage import default_storage
from django.conf import settings


def deleteMedia(media_url):
    try:
        if media_url:
            relative_path = media_url.replace(settings.MEDIA_URL, "")
            if default_storage.exists(relative_path):
                default_storage.delete(relative_path)

    except Exception as e:
        return f"Error deleting media: {e}"
