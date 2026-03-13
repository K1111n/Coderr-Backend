from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving reviews."""

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_rating(self, value):
        """Ensures rating is between 1 and 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def validate(self, data):
        """Prevents a reviewer from submitting duplicate reviews for the same business user."""
        request = self.context.get('request')
        if request and Review.objects.filter(reviewer=request.user, business_user=data.get('business_user')).exists():
            raise serializers.ValidationError('You have already reviewed this business user.')
        return data
