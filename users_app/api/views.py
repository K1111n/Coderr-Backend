# Third-party imports
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from users_app.api.permissions import IsOwner
from users_app.api.serializers import (
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    LoginSerializer,
    RegistrationSerializer,
    UserProfileSerializer,
)
from users_app.models import UserProfile


class RegistrationView(APIView):
    """Registers a new user and returns an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'username': user.username, 'email': user.email, 'user_id': user.id},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticates a user and returns an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'username': user.username, 'email': user.email, 'user_id': user.id},
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    """Retrieves or updates a user profile by user ID."""

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(user__id=pk)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        profile = self.get_object(pk)
        if profile is None:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk):
        profile = self.get_object(pk)
        if profile is None:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, profile)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


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
