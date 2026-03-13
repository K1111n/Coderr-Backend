from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users_app.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer
from users_app.models import UserProfile


class BusinessProfileListView(APIView):
    """Returns a list of all business user profiles."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns all profiles with type business."""
        profiles = UserProfile.objects.filter(type=UserProfile.BUSINESS)
        serializer = BusinessProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class CustomerProfileListView(APIView):
    """Returns a list of all customer user profiles."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns all profiles with type customer."""
        profiles = UserProfile.objects.filter(type=UserProfile.CUSTOMER)
        serializer = CustomerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
