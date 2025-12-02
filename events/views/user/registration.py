from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import EventRegistrationSerializer
from ..models.Event import Event
from ..models.EventRegistration import EventRegistration
from ..validations.event import RegisterEventValidator
from event_management.responseMessage import *


class RegisterEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            validator = RegisterEventValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_FAILED,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            event_id = validator.validated_data.get("eventId")
            try:
                event = Event.objects.get(id=event_id, isDeleted=False)
            except Event.DoesNotExist:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": EVENT_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if EventRegistration.objects.filter(
                userId=user, eventId=event, isDeleted=False
            ).exists():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": ALREADY_REGISTERED,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check capacity
            current_registrations = EventRegistration.objects.filter(
                eventId=event, isDeleted=False
            ).count()
            if current_registrations >= event.capacity:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Event capacity reached",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = {
                "userId": user.id,
                "eventId": event.id,
                "createdBy": str(user.id),
            }

            serializer = EventRegistrationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": EVENT_REGISTRATION_SUCCESS,
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
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
