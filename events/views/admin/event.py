from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import time
from ...serializers import EventSerializer
from ...models.EventRegistration import EventRegistration
from ...models.Event import Event
from ...validations.eventValidation import (
    CreateEventValidator,
    UpdateEventValidator,
    DeleteEventValidator,
)
from ...permissions import IsAdmin
from event_management.responseMessage import *
from ...models.Media import Media
from ...helpers.deleteMedia import deleteMedia
from django.db import transaction, connection
from event_management.constants import EVENT_FILTER_TYPE
from datetime import datetime


class CreateEventView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        try:
            data = {
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "datetime": request.data.get("datetime"),
                "venue": request.data.get("venue"),
                "capacity": request.data.get("capacity"),
                "imageId": request.data.get("imageId"),
                "userId": str(request.user.id),
                "createdBy": str(request.user.id),
            }

            validator = CreateEventValidator(data=data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": EVENT_CREATED,
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": VALIDATION_FAILED,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
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


class EventListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        try:
            current_time = datetime.now()
            filterType = request.data.get("filterType")
            search = request.data.get("search")

            countClause = """
                    SELECT COUNT(*) 
                    FROM event e
                """

            # Base query
            selectClause = """
                SELECT 
                    e."id",
                    e."title",
                    e."description",
                    e."datetime",
                    e."venue",
                    e."capacity",
                    e."imageId",
                    m."mediaUrl",
                    e."createdAt",
                    COALESCE(att.count, 0) AS attendee_count
                FROM event e
                LEFT JOIN (
                    SELECT "eventId", COUNT(*) AS count
                    FROM event_registration
                    WHERE "isDeleted" = FALSE
                    GROUP BY "eventId"
                ) att ON e."id" = att."eventId"
                LEFT JOIN media m ON e."imageId" = m."id"
            """

            # Dynamic WHERE conditions
            whereClause = ' WHERE e."isDeleted" = FALSE'
            params = []

            if filterType == EVENT_FILTER_TYPE["Upcoming"]:
                whereClause += ' AND e."datetime" >= %s'
                params.append(current_time)
            elif filterType == EVENT_FILTER_TYPE["Past"]:
                whereClause += ' AND e."datetime" < %s'
                params.append(current_time)

            if search:
                whereClause += " AND e.title ILIKE %s"
                params.append(f"%{search}%")

            # Ordering
            orderByClause = ' ORDER BY e."datetime" DESC'

            # Final query
            query = selectClause + whereClause + orderByClause
            countQuery = countClause + whereClause

            # Execute query
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]  # <-- column names
                events = [dict(zip(columns, row)) for row in cursor.fetchall()]

            with connection.cursor() as cursor:
                cursor.execute(countQuery, params)
                count = cursor.fetchone()[0]

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": EVENT_FETCH_SUCCESS,
                    "data": {"count": count, "events": events},
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


class UpdateEventView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        try:
            user = request.user
            validator = UpdateEventValidator(data=request.data, context={"user": user})
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            eventId = request.data["id"]
            event = Event.objects.get(
                id=eventId, createdBy=str(user.id), isDeleted=False
            )

            data = {}
            if "title" in request.data:
                data["title"] = request.data["title"]

            if "description" in request.data:
                data["description"] = request.data["description"]

            if "datetime" in request.data:
                data["datetime"] = request.data["datetime"]

            if "venue" in request.data:
                data["venue"] = request.data["venue"]

            if "capacity" in request.data:
                data["capacity"] = request.data["capacity"]

            data["updatedBy"] = str(user.id)
            data["updatedAt"] = int(time.time() * 1000)

            deletedMediaId = request.data.get("deletedMediaId")
            newImageId = request.data.get("imageId")

            # Upload new media only when old media is deleted
            if not deletedMediaId and newImageId:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "deletedMediaId is required to replace media.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Delete old media
            if deletedMediaId:
                media = Media.objects.get(id=deletedMediaId, isDeleted=False)

                # Delete file + soft delete record
                deleteMedia(media.mediaUrl)

                media.isDeleted = True
                media.deletedAt = int(time.time() * 1000)
                media.deletedBy = str(user.id)
                media.updatedAt = int(time.time() * 1000)
                media.save()

                data["imageId"] = request.data["imageId"]

            serializer = EventSerializer(event, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": EVENT_UPDATED,
                        "data": serializer.data,
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


class DeleteEventView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        try:
            user = request.user
            validator = DeleteEventValidator(data=request.data, context={"user": user})
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            event_id = request.data.get("id")
            try:
                with transaction.atomic():
                    # lock event row for update
                    event = Event.objects.select_for_update().get(
                        id=event_id, createdBy=str(user.id), isDeleted=False
                    )

                    event.deletedAt = int(time.time() * 1000)
                    event.deletedBy = str(user.id)
                    event.updatedAt = int(time.time() * 1000)
                    event.isDeleted = True
                    event.save()

                    # handle media if present
                    if event.imageId:
                        media = Media.objects.select_for_update().get(
                            id=event.imageId.id, isDeleted=False
                        )

                        # remove external/local file (function should handle failures)
                        deleteMedia(media.mediaUrl)

                        media.isDeleted = True
                        media.deletedAt = int(time.time() * 1000)
                        media.deletedBy = str(user.id)
                        media.updatedAt = int(time.time() * 1000)
                        media.save()

            except Exception as error:
                print(f"Unexpected error in Transaction: {error}")
                return Response(
                    {
                        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": WENTS_WRONG,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"status": status.HTTP_200_OK, "message": EVENT_DELETED},
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
