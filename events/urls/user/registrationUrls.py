from django.urls import path
from events.views.user.registration import RegisterEventView

urlpatterns = [
    path("register-event/", RegisterEventView.as_view(), name="user-register-event"),
]
