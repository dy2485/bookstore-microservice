from rest_framework import serializers
from .models import Order, OrderItem, OrderAddress, OrderStatusHistory, OrderCoupon, OrderTransaction

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = '__all__'

class OrderCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCoupon
        fields = '__all__'

class OrderTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTransaction
        fields = '__all__'
