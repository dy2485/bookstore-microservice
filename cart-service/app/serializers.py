from rest_framework import serializers
from .models import Cart, CartItem, CartPromo, CartLock

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class CartPromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartPromo
        fields = '__all__'

class CartLockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartLock
        fields = '__all__'
