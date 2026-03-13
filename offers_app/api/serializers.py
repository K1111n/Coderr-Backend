from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for a single offer detail (basic, standard, premium)."""

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    """Serializer that exposes only the id and URL of an offer detail."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """Returns the absolute URL for the offer detail endpoint."""
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/offerdetails/{obj.id}/')


class UserDetailsSerializer(serializers.Serializer):
    """Serializer for basic user identity fields."""

    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for listing offers with aggregated price and delivery info."""

    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details',
        ]

    def get_min_price(self, obj):
        """Returns the lowest price across all offer details."""
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.price for d in details)

    def get_min_delivery_time(self, obj):
        """Returns the shortest delivery time across all offer details."""
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.delivery_time_in_days for d in details)

    def get_user_details(self, obj):
        """Returns basic identity info for the offer's creator."""
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new offer with exactly 3 details."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        """Ensures exactly 3 details with types basic, standard, and premium."""
        if len(value) != 3:
            raise serializers.ValidationError('An offer must have exactly 3 details.')
        types = [d['offer_type'] for d in value]
        if sorted(types) != ['basic', 'premium', 'standard']:
            raise serializers.ValidationError('Details must include basic, standard and premium.')
        return value

    def create(self, validated_data):
        """Creates the offer and its associated detail objects."""
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single offer with aggregated price and delivery info."""

    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time',
        ]

    def get_min_price(self, obj):
        """Returns the lowest price across all offer details."""
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.price for d in details)

    def get_min_delivery_time(self, obj):
        """Returns the shortest delivery time across all offer details."""
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.delivery_time_in_days for d in details)


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Serializer for partially updating an offer and its details."""

    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        """Ensures each detail includes an offer_type."""
        for detail in value:
            if not detail.get('offer_type'):
                raise serializers.ValidationError('Each detail must include an offer_type.')
        return value

    def update(self, instance, validated_data):
        """Updates offer fields and patches matching detail records by offer_type."""
        details_data = validated_data.pop('details', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            OfferDetail.objects.filter(offer=instance, offer_type=offer_type).update(**detail_data)
        return instance
