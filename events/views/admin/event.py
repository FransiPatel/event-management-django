from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import time
from ..serializers import EventSerializer
from ..models.Event import Event
from ..validations.event import (
    CreateEventValidator,
    UpdateEventValidator,
    DeleteEventValidator,
)
from ..permissions import IsAdmin
from event_management.responseMessage import *


class CreateEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = {
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "datetime": request.data.get("datetime"),
                "venue": request.data.get("venue"),
                "capacity": request.data.get("capacity"),
                "imageId": request.data.get("imageId"),
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # filter params: venue, upcoming, past, date range can be added later
            events = Event.objects.filter(createdBy=str(user.id), isDeleted=False)
            data = list(
                events.order_by("-createdAt").values(
                    "id",
                    "title",
                    "description",
                    "datetime",
                    "venue",
                    "capacity",
                    "imageId",
                    "createdAt",
                )
            )
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": EVENT_FETCH_SUCCESS,
                    "data": {"count": events.count(), "events": data},
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

            event_id = validator.validated_data.get("id")
            event = Event.objects.get(
                id=event_id, createdBy=str(user.id), isDeleted=False
            )

            data = {}
            for field in (
                "title",
                "description",
                "datetime",
                "venue",
                "capacity",
                "imageId",
            ):
                if field in request.data:
                    data[field] = request.data.get(field)

            data["updatedBy"] = str(user.id)
            data["updatedAt"] = int(time.time() * 1000)

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
            event = Event.objects.get(
                id=event_id, createdBy=str(user.id), isDeleted=False
            )

            # Soft delete: set deletedAt, deletedBy and updatedAt
            event.deletedAt = int(time.time() * 1000)
            event.deletedBy = str(user.id)
            event.updatedAt = int(time.time() * 1000)
            event.isDeleted = True
            event.save()

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
