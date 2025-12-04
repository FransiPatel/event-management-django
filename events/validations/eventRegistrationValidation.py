from rest_framework import serializers
from event_management.responseMessage import *


class RegisterEventValidator(serializers.Serializer):
    eventId = serializers.CharField(required=True)
