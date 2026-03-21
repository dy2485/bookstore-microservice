from rest_framework import serializers
from .models import Customer, CustomerAddress, CustomerProfile, CustomerActivity, CustomerWishlist

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

class CustomerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerActivity
        fields = '__all__'

class CustomerWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWishlist
        fields = '__all__'
