# Third-party imports
from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allows access only to users with a customer profile."""

    message = 'Only customer users can create reviews.'

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'


class IsReviewer(BasePermission):
    """Allows access only to the reviewer who created the review."""

    message = 'Only the author of this review can perform this action.'

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
