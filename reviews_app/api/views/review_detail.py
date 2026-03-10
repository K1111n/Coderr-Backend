# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from reviews_app.api.permissions import IsReviewer
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewDetailView(APIView):
    """Updates or deletes a specific review. Only the reviewer can do this."""

    permission_classes = [IsAuthenticated, IsReviewer]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    def patch(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, review)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
