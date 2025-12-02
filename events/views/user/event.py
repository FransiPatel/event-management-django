from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from datetime import datetime
from ...models.Event import Event
from event_management.responseMessage import *


class UserEventListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get all available events (not deleted)
            current_time = datetime.now()

            # Filter: upcoming events by default, can be extended
            filter_type = request.query_params.get("filter", "all")

            events_query = Event.objects.filter(isDeleted=False).annotate(
                attendee_count=Count(
                    "registrations", filter=Q(registrations__isDeleted=False)
                )
            )

            if filter_type == "upcoming":
                events_query = events_query.filter(datetime__gte=current_time)
            elif filter_type == "past":
                events_query = events_query.filter(datetime__lt=current_time)

            events = events_query.values(
                "id",
                "title",
                "description",
                "datetime",
                "venue",
                "capacity",
                "imageId",
                "createdAt",
                "attendee_count",
            ).order_by("-datetime")

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
