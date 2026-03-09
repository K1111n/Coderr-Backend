# Third-party imports
from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """Allows access only to users with a business profile."""

    message = 'Only business users can perform this action.'

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'business'


class IsOfferOwner(BasePermission):
    """Allows access only to the owner of the offer."""

    message = 'Only the owner of this offer can perform this action.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
