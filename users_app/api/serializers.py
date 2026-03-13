from django.contrib.auth.models import User
from rest_framework import serializers

from users_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user with a profile type."""

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """Ensures both password fields match."""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({'repeated_password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        """Creates the user and associated profile with the given type."""
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, type=user_type)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for validating login credentials."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating a user's own profile."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at',
        ]
        read_only_fields = ['user', 'type', 'created_at']

    def update(self, instance, validated_data):
        """Updates profile and syncs changed fields to the related User model."""
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return super().update(instance, validated_data)


class BusinessProfileSerializer(serializers.ModelSerializer):
    """Serializer for reading a business user's public profile."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description', 'working_hours', 'type',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer for reading a customer user's public profile."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']
