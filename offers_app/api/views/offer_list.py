# Standard library
from django.db.models import Min, Q

# Third-party imports
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from offers_app.api.permissions import IsBusinessUser
from offers_app.api.serializers import OfferCreateSerializer, OfferListSerializer
from offers_app.models import Offer


class OfferPagination(PageNumberPagination):
    """Pagination class that allows page_size to be set via query param."""

    page_size = 6
    page_size_query_param = 'page_size'


class OfferListCreateView(APIView):
    """Lists all offers with filtering/ordering or creates a new offer."""

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def _apply_filters(self, queryset, params):
        """Filters by creator_id and search term."""
        if creator_id := params.get('creator_id'):
            queryset = queryset.filter(user__id=creator_id)
        if search := params.get('search'):
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return queryset

    def _apply_price_and_delivery_filters(self, queryset, params):
        """Annotates and filters by min_price and max_delivery_time."""
        ordering = params.get('ordering', '')
        if params.get('min_price') or 'min_price' in ordering:
            queryset = queryset.annotate(min_p=Min('details__price'))
        if params.get('max_delivery_time'):
            queryset = queryset.annotate(min_d=Min('details__delivery_time_in_days'))
        if params.get('min_price'):
            try:
                queryset = queryset.filter(min_p__gte=float(params['min_price']))
            except (ValueError, TypeError):
                raise ValueError('min_price')
        if params.get('max_delivery_time'):
            try:
                queryset = queryset.filter(min_d__lte=int(params['max_delivery_time']))
            except (ValueError, TypeError):
                raise ValueError('max_delivery_time')
        return queryset

    def _apply_ordering(self, queryset, params):
        """Orders the queryset by updated_at or min_price."""
        ordering = params.get('ordering', '-updated_at')
        order_map = {
            'min_price': 'min_p', '-min_price': '-min_p',
            'updated_at': 'updated_at', '-updated_at': '-updated_at',
        }
        return queryset.order_by(order_map.get(ordering, '-updated_at'))

    def get(self, request):
        queryset = Offer.objects.all()
        queryset = self._apply_filters(queryset, request.query_params)
        try:
            queryset = self._apply_price_and_delivery_filters(queryset, request.query_params)
        except ValueError as e:
            return Response({'error': f'Invalid value for {e}.'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self._apply_ordering(queryset, request.query_params)
        paginator = OfferPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OfferListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OfferCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
