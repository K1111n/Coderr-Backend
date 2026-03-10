# Standard library
from django.db.models import Avg

# Third-party imports
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from offers_app.models import Offer
from reviews_app.models import Review
from users_app.models import UserProfile


class BaseInfoView(APIView):
    """Returns aggregated platform statistics. No authentication required."""

    permission_classes = [AllowAny]

    def get(self, request):
        avg = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        return Response({
            'review_count': Review.objects.count(),
            'average_rating': round(avg, 1),
            'business_profile_count': UserProfile.objects.filter(type=UserProfile.BUSINESS).count(),
            'offer_count': Offer.objects.count(),
        })
