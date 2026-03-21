from rest_framework import serializers
from .models import Shipment, ShipmentItem, ShippingRate, ShippingAddress, ShipmentHistory

class ShipmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentItem
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    items = ShipmentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'

class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class ShipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentHistory
        fields = '__all__'
