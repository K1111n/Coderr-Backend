# Third-party imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from offers_app.models import OfferDetail
from orders_app.api.permissions import IsBusinessUser, IsCustomerUser
from orders_app.api.serializers import OrderCreateSerializer, OrderSerializer
from orders_app.models import Order


class OrderListCreateView(APIView):
    """Lists orders for the current user or creates a new order."""

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get(self, request):
        orders = Order.objects.filter(
            customer_user=request.user
        ) | Order.objects.filter(business_user=request.user)
        serializer = OrderSerializer(orders.distinct(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        offer_detail_id = serializer.validated_data['offer_detail_id']
        try:
            offer_detail = OfferDetail.objects.get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({'error': 'Offer detail not found.'}, status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    """Updates the status of an order (business only) or deletes it (admin only)."""

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), IsBusinessUser()]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def patch(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
