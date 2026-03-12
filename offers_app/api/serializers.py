from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/offerdetails/{obj.id}/')


class UserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
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
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.price for d in details)

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.delivery_time_in_days for d in details)

    def get_user_details(self, obj):
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError('An offer must have exactly 3 details.')
        types = [d['offer_type'] for d in value]
        if sorted(types) != ['basic', 'premium', 'standard']:
            raise serializers.ValidationError('Details must include basic, standard and premium.')
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class OfferRetrieveSerializer(serializers.ModelSerializer):
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
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.price for d in details)

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        if not details.exists():
            return None
        return min(d.delivery_time_in_days for d in details)


class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        for detail in value:
            if not detail.get('offer_type'):
                raise serializers.ValidationError('Each detail must include an offer_type.')
        return value

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            OfferDetail.objects.filter(offer=instance, offer_type=offer_type).update(**detail_data)
        return instance
