from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from event_management.responseMessage import *
from ...helpers.uploadMedia import uploadMedia
from ...validations.mediaValidation import FileUploadValidator


class UploadMediaView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            user = request.user
            file = request.FILES.get("file")
            uploadType = request.data.get("typeOfFile")
            duration = int(request.data.get("duration", 0))

            # Validate file with custom validator
            FileUploadValidator.validate(uploadType, file)

            # Upload file
            result = uploadMedia(user, file)

            if result.get("ok"):
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": MEDIA_UPLOAD_SUCCESS,
                        "data": {
                            **result.get("data"),
                            "typeOfFile": uploadType,
                            "duration": duration,
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": VALIDATION_FAILED,
                    "errors": result.get("errors"),
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
