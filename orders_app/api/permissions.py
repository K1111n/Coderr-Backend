# Third-party imports
from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allows access only to users with a customer profile."""

    message = 'Only customer users can perform this action.'

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'


class IsBusinessUser(BasePermission):
    """Allows access only to users with a business profile."""

    message = 'Only business users can perform this action.'

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'business'
