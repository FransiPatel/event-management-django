USER_PROFILE_TYPE = {
    "Admin": "admin",
    "User": "user",
}

PASSWORD_REGEX = r'^[A-Za-z\d!@#*\$%^&()_+\-=\[\]{};\':"\\|,.<>\/?]{8,15}$'

ALLOWED_MIME_PREFIXES = ("image/", "video/")

ALLOWED_FILE_TYPES = {
    "Jpeg": "jpeg",
    "Jpg": "jpg",
    "Png": "png",
    "Gif": "gif",
    "Svg": "svg",
    "Mp4": "mp4",
    "Mov": "mov",
    "Avi": "avi",
    "Mkv": "mkv",
}

USER_MEDIA_UPLOAD_TYPE = {
    "EventCoverImage": "eventCoverImage",
}

EVENT_FILTER_TYPE = {
    "Upcoming": "upcoming",
    "Past": "past",
}
