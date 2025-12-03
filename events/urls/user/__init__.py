from django.urls import include, path

urlpatterns = [
    path("", include("events.urls.user.eventUrls")),
    path("", include("events.urls.user.mediaUrls")),
    path("", include("events.urls.user.registrationUrls")),
]
