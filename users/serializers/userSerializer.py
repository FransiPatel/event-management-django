from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "firstName", "lastName", "password", "username"]

    def create(self, validated_data):
        # Hash the password manually here
        validated_data["password"] = make_password(validated_data["password"])

        # Create user normally
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            firstName=validated_data["firstName"],
            lastName=validated_data["lastName"],
            password=validated_data["password"],
        )
        return user
