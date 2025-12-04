from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ...serializers.userSerializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ...validations.auth import (
    LoginValidator,
    RegisterValidator,
    RegisterSocialValidator,
)
from event_management.responseMessage import *


class RegisterUser(APIView):
    def post(self, request):
        try:
            validator = RegisterValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_ERROR,
                        "data": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": USER_REGISTERED,
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
                    "data": {},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RegisterUserSocial(APIView):
    def post(self, request):
        try:
            validator = RegisterSocialValidator(data=request.data)
            if not validator.is_valid():
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": VALIDATION_ERROR,
                        "data": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": USER_REGISTERED,
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
                    "data": {},
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
                        "data": validator.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = request.data["email"]
            password = request.data["password"]

            user = authenticate(email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                # Store tokens in user model
                user.token = str(access)
                user.refreshToken = str(refresh)
                user.save(update_fields=["token", "refreshToken"])

                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": LOGIN_SUCCESS,
                        "data": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
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
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfileUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": PROFILE_FETCHED,
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


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Refresh token is required.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Logout successful.",
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid or expired refresh token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
