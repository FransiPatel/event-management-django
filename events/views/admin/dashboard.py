from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from datetime import datetime
import time
from ...models.Event import Event
from ...models.EventRegistration import EventRegistration
from ...permissions import IsAdmin
from event_management.responseMessage import *


class AdminDashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            current_time = datetime.now()

            total_events = Event.objects.filter(isDeleted=False).count()
            total_registrations = EventRegistration.objects.filter(
                isDeleted=False
            ).count()

            upcoming_events_count = Event.objects.filter(
                isDeleted=False, datetime__gte=current_time
            ).count()

            past_events_count = Event.objects.filter(
                isDeleted=False, datetime__lt=current_time
            ).count()

            thirty_days_ago = int((time.time() - 30 * 24 * 60 * 60) * 1000)

            recent_registrations = EventRegistration.objects.filter(
                isDeleted=False, createdAt__gte=thirty_days_ago
            ).count()

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Summary fetched successfully",
                    "data": {
                        "total_events": total_events,
                        "total_registrations": total_registrations,
                        "upcoming_events_count": upcoming_events_count,
                        "past_events_count": past_events_count,
                        "recent_registrations_30_days": recent_registrations,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminUpcomingEventsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            current_time = datetime.now()

            upcoming_events = (
                Event.objects.filter(isDeleted=False, datetime__gte=current_time)
                .annotate(
                    attendee_count=Count(
                        "registrations",
                        filter=Q(registrations__isDeleted=False),
                    )
                )
                .values(
                    "id",
                    "title",
                    "description",
                    "datetime",
                    "venue",
                    "capacity",
                    "attendee_count",
                    "createdAt",
                )
                .order_by("datetime")
            )

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Upcoming events fetched",
                    "data": list(upcoming_events),
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
