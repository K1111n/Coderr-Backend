# Third-party imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from orders_app.models import Order


class OrderCountView(APIView):
    """Returns the number of in-progress orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        if not User.objects.filter(pk=business_user_id).exists():
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)
        count = Order.objects.filter(business_user__id=business_user_id, status=Order.IN_PROGRESS).count()
        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    """Returns the number of completed orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        if not User.objects.filter(pk=business_user_id).exists():
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)
        count = Order.objects.filter(business_user__id=business_user_id, status=Order.COMPLETED).count()
        return Response({'completed_order_count': count})
