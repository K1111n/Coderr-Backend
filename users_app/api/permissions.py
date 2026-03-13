from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allows access only to the owner of the profile object."""

    message = 'You do not have permission to edit this profile.'

    def has_object_permission(self, request, view, obj):
        """Returns True if the requesting user is the profile owner."""
        return obj.user == request.user
