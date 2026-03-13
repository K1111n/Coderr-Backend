from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.api.permissions import IsBusinessUser
from orders_app.api.serializers import OrderSerializer
from orders_app.models import Order


class OrderDetailView(APIView):
    """Updates the status of an order (business only) or deletes it (admin only)."""

    def initial(self, request, *args, **kwargs):
        """Raises 404 before permission checks if the order does not exist."""
        pk = kwargs.get('pk')
        if pk and not Order.objects.filter(pk=pk).exists():
            raise NotFound('Order not found.')
        super().initial(request, *args, **kwargs)

    def get_permissions(self):
        """Returns IsAdminUser for DELETE, IsBusinessUser for PATCH."""
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), IsBusinessUser()]

    def get_object(self, pk):
        """Returns the order with the given pk, or None if not found."""
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def patch(self, request, pk):
        """Partially updates an order. Only accessible by business users."""
        order = self.get_object(pk)
        if order is None:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """Deletes an order. Only accessible by admins."""
        order = self.get_object(pk)
        if order is None:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
