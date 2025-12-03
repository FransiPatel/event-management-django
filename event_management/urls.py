from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("users.urls")),
    # Admin event routes
    path("api/admin/event/", include("events.urls.admin")),
    # User event routes
    path("api/user/event/", include("events.urls.user")),
]
