# Admin views
from .admin import (
    CreateEventView,
    UpdateEventView,
    DeleteEventView,
    AdminDashboardView,
    AdminEventListView,
    AdminEventDetailsView,
)

# User views
from .user import RegisterEventView, UploadMediaView, UserEventListView

__all__ = [
    # Admin views
    "CreateEventView",
    "UpdateEventView",
    "DeleteEventView",
    "AdminDashboardView",
    "AdminEventListView",
    "AdminEventDetailsView",
    # User views
    "RegisterEventView",
    "UploadMediaView",
    "UserEventListView",
]
