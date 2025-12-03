from rest_framework import serializers
from event_management.responseMessage import *


class EventDashboardValidator(serializers.Serializer):
    startDate = serializers.DateTimeField(required=False)
    endDate = serializers.DateTimeField(required=False)
    venue = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    recentDays = serializers.IntegerField(required=False, min_value=1)

    def validate(self, attrs):
        start = attrs.get("startDate")
        end = attrs.get("endDate")
        recent = attrs.get("recentDays")

        if start and end and start > end:
            raise serializers.ValidationError("startDate must be before endDate")

        # recentDays cannot be combined with explicit date range
        if recent and (start or end):
            raise serializers.ValidationError(
                "recentDays cannot be used with startDate/endDate"
            )

        return attrs
