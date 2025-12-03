from django.urls import path
from events.views.admin.event import (
    CreateEventView,
    UpdateEventView,
    DeleteEventView,
    EventListView,
)

urlpatterns = [
    path("list/", EventListView.as_view(), name="admin-event-list"),
    path("create-event/", CreateEventView.as_view(), name="admin-create-event"),
    path("update-event/", UpdateEventView.as_view(), name="admin-update-event"),
    path("delete-event/", DeleteEventView.as_view(), name="admin-delete-event"),
]
