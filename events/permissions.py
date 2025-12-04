from rest_framework.permissions import BasePermission
from event_management.constants import USER_PROFILE_TYPE


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.profileType == USER_PROFILE_TYPE["Admin"]
        )
