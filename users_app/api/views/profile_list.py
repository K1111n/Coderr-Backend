# Third-party imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from users_app.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer
from users_app.models import UserProfile


class BusinessProfileListView(APIView):
    """Returns a list of all business user profiles."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.filter(type=UserProfile.BUSINESS)
        serializer = BusinessProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class CustomerProfileListView(APIView):
    """Returns a list of all customer user profiles."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.filter(type=UserProfile.CUSTOMER)
        serializer = CustomerProfileSerializer(profiles, many=True)
        return Response(serializer.data)
