from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings
import time
import os
from ..models.Media import Media
from ..serializers import MediaSerializer
from event_management.responseMessage import *


class UploadMediaView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            user = request.user
            file = request.FILES.get("file")

            if not file:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": FILE_REQUIRED,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT)
            os.makedirs(upload_dir, exist_ok=True)

            # Generate unique filename
            timestamp = int(time.time() * 1000)
            file_extension = os.path.splitext(file.name)[1]
            unique_filename = f"{timestamp}_{file.name}"

            # Save file
            file_path = os.path.join("uploads", unique_filename)
            saved_path = default_storage.save(file_path, file)

            # Get file type
            file_type = file.content_type or "unknown"

            # Create media record
            media_data = {
                "mediaUrl": f"{settings.MEDIA_URL}{unique_filename}",
                "mediaName": file.name,
                "type": file_type,
                "isExternal": False,
                "source": "upload",
                "createdBy": str(user.id),
            }

            serializer = MediaSerializer(data=media_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": MEDIA_UPLOAD_SUCCESS,
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                # Delete uploaded file if serializer fails
                default_storage.delete(saved_path)
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
