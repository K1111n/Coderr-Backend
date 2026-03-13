from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users_app.api.permissions import IsOwner
from users_app.api.serializers import UserProfileSerializer
from users_app.models import UserProfile


class ProfileView(APIView):
    """Retrieves or updates a user profile by user ID."""

    def get_permissions(self):
        """Returns IsOwner for PATCH, IsAuthenticated for GET."""
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        """Returns the profile for the given user pk, or None if not found."""
        try:
            return UserProfile.objects.get(user__id=pk)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        """Returns a single user profile by pk."""
        profile = self.get_object(pk)
        if profile is None:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk):
        """Partially updates a user profile. Only accessible by the profile owner."""
        profile = self.get_object(pk)
        if profile is None:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, profile)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)
