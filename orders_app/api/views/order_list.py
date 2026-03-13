from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import OfferDetail
from orders_app.api.permissions import IsCustomerUser
from orders_app.api.serializers import OrderCreateSerializer, OrderSerializer
from orders_app.models import Order


class OrderListCreateView(APIView):
    """Lists orders for the current user or creates a new order."""

    def get_permissions(self):
        """Returns IsCustomerUser for POST, IsAuthenticated for GET."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get(self, request):
        """Returns all orders belonging to the current user as customer or business."""
        orders = Order.objects.filter(
            customer_user=request.user
        ) | Order.objects.filter(business_user=request.user)
        serializer = OrderSerializer(orders.distinct(), many=True)
        return Response(serializer.data)

    def post(self, request):
        """Creates a new order from an offer detail. Only accessible by customer users."""
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
