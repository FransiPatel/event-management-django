from django.urls import path
from .views import (
    # Admin views
    CreateEventView,
    UpdateEventView,
    DeleteEventView,
    AdminDashboardView,
    AdminEventListView,
    AdminEventDetailsView,
    # User views
    RegisterEventView,
    UploadMediaView,
    UserEventListView,
)

app_name = "events"

urlpatterns = [
    # Admin routes
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("admin/events/", AdminEventListView.as_view(), name="admin-event-list"),
    path(
        "admin/events/<uuid:event_id>/",
        AdminEventDetailsView.as_view(),
        name="admin-event-details",
    ),
    path("admin/create-event/", CreateEventView.as_view(), name="create-event"),
    path("admin/update-event/", UpdateEventView.as_view(), name="update-event"),
    path("admin/delete-event/", DeleteEventView.as_view(), name="delete-event"),
    # User routes
    path("list/", UserEventListView.as_view(), name="event-list"),
    path("register-event/", RegisterEventView.as_view(), name="register-event"),
    path("upload-media/", UploadMediaView.as_view(), name="upload-media"),
]
