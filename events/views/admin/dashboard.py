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


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            # Total number of events created
            total_events = Event.objects.filter(isDeleted=False).count()

            # Total number of registrations
            total_registrations = EventRegistration.objects.filter(
                isDeleted=False
            ).count()

            # Number of attendees per event
            events_with_attendees = (
                Event.objects.filter(isDeleted=False)
                .annotate(
                    attendee_count=Count(
                        "registrations", filter=Q(registrations__isDeleted=False)
                    )
                )
                .values("id", "title", "datetime", "capacity", "attendee_count")
                .order_by("-createdAt")
            )

            # Upcoming events (events with datetime in the future)
            current_time = datetime.now()
            upcoming_events = (
                Event.objects.filter(isDeleted=False, datetime__gte=current_time)
                .annotate(
                    attendee_count=Count(
                        "registrations", filter=Q(registrations__isDeleted=False)
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

            # Registration trends (last 30 days)
            thirty_days_ago = int((time.time() - 30 * 24 * 60 * 60) * 1000)
            recent_registrations = EventRegistration.objects.filter(
                isDeleted=False, createdAt__gte=thirty_days_ago
            ).count()

            # Events by status
            past_events_count = Event.objects.filter(
                isDeleted=False, datetime__lt=current_time
            ).count()
            upcoming_events_count = Event.objects.filter(
                isDeleted=False, datetime__gte=current_time
            ).count()

            dashboard_data = {
                "summary": {
                    "total_events": total_events,
                    "total_registrations": total_registrations,
                    "upcoming_events_count": upcoming_events_count,
                    "past_events_count": past_events_count,
                    "recent_registrations_30_days": recent_registrations,
                },
                "events_with_attendees": list(events_with_attendees),
                "upcoming_events": list(upcoming_events),
            }

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Dashboard data fetched successfully",
                    "data": dashboard_data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminEventListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            # Get all events with registration count
            events = (
                Event.objects.filter(isDeleted=False)
                .annotate(
                    attendee_count=Count(
                        "registrations", filter=Q(registrations__isDeleted=False)
                    )
                )
                .values(
                    "id",
                    "title",
                    "description",
                    "datetime",
                    "venue",
                    "capacity",
                    "imageId",
                    "createdAt",
                    "createdBy",
                    "attendee_count",
                )
                .order_by("-createdAt")
            )

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": EVENT_FETCH_SUCCESS,
                    "data": {"count": events.count(), "events": list(events)},
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminEventDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, event_id):
        try:
            # Get event details
            event = Event.objects.filter(id=event_id, isDeleted=False).first()

            if not event:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": EVENT_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Get registered users for this event
            registrations = EventRegistration.objects.filter(
                eventId=event, isDeleted=False
            ).select_related("userId")

            registered_users = []
            for reg in registrations:
                if reg.userId:
                    registered_users.append(
                        {
                            "registration_id": str(reg.id),
                            "user_id": str(reg.userId.id),
                            "username": reg.userId.username,
                            "email": reg.userId.email,
                            "firstName": reg.userId.firstName,
                            "lastName": reg.userId.lastName,
                            "registered_at": reg.createdAt,
                        }
                    )

            event_data = {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "datetime": event.datetime,
                "venue": event.venue,
                "capacity": event.capacity,
                "imageId": str(event.imageId.id) if event.imageId else None,
                "createdAt": event.createdAt,
                "total_registrations": len(registered_users),
                "registered_users": registered_users,
            }

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Event details fetched successfully",
                    "data": event_data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
