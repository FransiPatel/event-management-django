from django.urls import include, path

urlpatterns = [
    path("", include("events.urls.admin.eventUrls")),
    path("", include("events.urls.admin.dashboardUrls")),
]
