# Admin views
from .admin import (
    CreateEventView,
    UpdateEventView,
    DeleteEventView,
    EventListView,
    AdminEventDetailsView,
    AdminDashboardSummaryView,
    AdminUpcomingEventsView,
)

# User views
from .user import RegisterEventView, UploadMediaView, UserEventListView

__all__ = [
    # Admin views
    "CreateEventView",
    "UpdateEventView",
    "DeleteEventView",
    "EventListView",
    "AdminEventDetailsView",
    "AdminDashboardSummaryView",
    "AdminUpcomingEventsView",
    # User views
    "RegisterEventView",
    "UploadMediaView",
    "UserEventListView",
]
