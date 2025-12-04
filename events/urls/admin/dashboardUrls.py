from django.urls import path
from events.views.admin.dashboard import (
    AdminDashboardSummaryView,
    AdminUpcomingEventsView,
)

urlpatterns = [
    path("dashboard/summary/", AdminDashboardSummaryView.as_view()),
    path("dashboard/upcoming-events/", AdminUpcomingEventsView.as_view()),
]
