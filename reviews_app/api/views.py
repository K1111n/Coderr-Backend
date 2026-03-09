# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from reviews_app.api.permissions import IsCustomerUser, IsReviewer
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewListCreateView(APIView):
    """Lists all reviews with optional filters or creates a new review."""

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def _build_queryset(self, params):
        """Filters and orders the review queryset based on query params."""
        queryset = Review.objects.all()
        if business_user_id := params.get('business_user_id'):
            queryset = queryset.filter(business_user__id=business_user_id)
        if reviewer_id := params.get('reviewer_id'):
            queryset = queryset.filter(reviewer__id=reviewer_id)
        ordering = params.get('ordering', '-updated_at')
        if ordering in ('updated_at', '-updated_at', 'rating', '-rating'):
            queryset = queryset.order_by(ordering)
        return queryset

    def get(self, request):
        queryset = self._build_queryset(request.query_params)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(reviewer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
