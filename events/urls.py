from django.urls import path
from .views import CreateEventView, EventListView, UpdateEventView, DeleteEventView

app_name = "events"

urlpatterns = [
    path("create-event/", CreateEventView.as_view(), name="create-event"),
    path("list/", EventListView.as_view(), name="event-list"),
    path("update-event/", UpdateEventView.as_view(), name="update-event"),
    path("delete-event/", DeleteEventView.as_view(), name="delete-event"),
]
