from django.urls import path
from events.views.user.event import (
    UserEventListView,
    CreateEventView,
    EventListView,
    UpdateEventView,
    DeleteEventView,
)

urlpatterns = [
    path("user-list/", UserEventListView.as_view(), name="user-event-list"),
    path("list/", EventListView.as_view(), name="event-list"),
    path("create-event/", CreateEventView.as_view(), name="user-create-event"),
    path("update-event/", UpdateEventView.as_view(), name="user-update-event"),
    path("delete-event/", DeleteEventView.as_view(), name="user-delete-event"),
]
