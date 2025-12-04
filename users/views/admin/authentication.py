from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ...serializers.userSerializer import UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from ...validations.auth import LoginValidator, CreateAdminValidator
from event_management.responseMessage import *
from event_management.constants import USER_PROFILE_TYPE

User = get_user_model()


class CreateAdminUser(APIView):
    def post(self, request):
        try:
            validator = CreateAdminValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_ERROR,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create admin user
            user_data = {
                "email": request.data.get("email"),
                "password": request.data.get("password"),
                "firstName": request.data.get("firstName"),
                "lastName": request.data.get("lastName"),
                "username": request.data.get("username"),
                "profileType": USER_PROFILE_TYPE["Admin"],
            }

            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data.get("password"))
                user.save()

                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": "Admin user created successfully",
                        "data": UserSerializer(user).data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": VALIDATION_ERROR,
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
                    "data": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginUser(APIView):
    def post(self, request):
        try:
            validator = LoginValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_ERROR,
                        "errors": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = request.data.get("email")
            password = request.data.get("password")

            user = authenticate(request, username=email, password=password)

            if not user:
                return Response(
                    {
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "message": "Invalid email or password",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Login successful",
                    "data": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "user": UserSerializer(user).data,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                    "data": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Logout successful",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": WENTS_WRONG,
                    "data": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
