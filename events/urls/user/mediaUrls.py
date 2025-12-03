from django.urls import path
from events.views.user.media import UploadMediaView

urlpatterns = [
    path("upload-media/", UploadMediaView.as_view(), name="user-upload-media"),
]
