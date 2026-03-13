from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.api.permissions import IsOfferOwner
from offers_app.api.serializers import OfferDetailSerializer, OfferRetrieveSerializer, OfferUpdateSerializer
from offers_app.models import Offer, OfferDetail


class OfferDetailView(APIView):
    """Retrieves, updates or deletes a specific offer."""

    def get_permissions(self):
        """Returns IsOfferOwner for PATCH and DELETE, IsAuthenticated for GET."""
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        """Returns the offer with the given pk, or None if not found."""
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return None

    def get(self, request, pk):
        """Returns a single offer by pk."""
        offer = self.get_object(pk)
        if offer is None:
            return Response({'error': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OfferRetrieveSerializer(offer, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        """Partially updates an offer. Only accessible by the offer owner."""
        offer = self.get_object(pk)
        if offer is None:
            return Response({'error': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, offer)
        serializer = OfferUpdateSerializer(offer, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        updated_offer = serializer.save()
        return Response(OfferUpdateSerializer(updated_offer).data)

    def delete(self, request, pk):
        """Deletes an offer. Only accessible by the offer owner."""
        offer = self.get_object(pk)
        if offer is None:
            return Response({'error': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailItemView(APIView):
    """Retrieves a specific offer detail by ID."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Returns a single offer detail by pk."""
        try:
            detail = OfferDetail.objects.get(pk=pk)
        except OfferDetail.DoesNotExist:
            return Response({'error': 'Offer detail not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OfferDetailSerializer(detail)
        return Response(serializer.data)
