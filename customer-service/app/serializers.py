from rest_framework import serializers
from .models import Customer, CustomerAddress, CustomerProfile, CustomerActivity, CustomerWishlist


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for customer basic info
    """
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'name', 'phone', 'address', 'dob', 'gender']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """Validate name is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError('Name cannot be empty')
        return value.strip()
    
    def validate_phone(self, value):
        """Validate phone format"""
        if value and len(value) < 10:
            raise serializers.ValidationError('Phone must be at least 10 characters')
        return value


class CustomerAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for customer addresses
    """
    class Meta:
        model = CustomerAddress
        fields = ['id', 'customer', 'label', 'street', 'city', 'province', 'country', 'is_default']
        read_only_fields = ['id', 'customer']
    
    def validate(self, attrs):
        """Ensure at least one address is default if multiple exist"""
        if attrs.get('is_default'):
            # Check if this is a new address or update
            if self.instance is None:
                # New address
                customer = self.context.get('customer')
                if customer and customer.customeraddress_set.filter(is_default=True).exists():
                    # We'll handle this in view to set all others to False
                    pass
        return attrs


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for extended customer profile
    """
    customer_info = CustomerSerializer(source='customer', read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['id', 'customer', 'customer_info', 'bio', 'prefer_genres', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for customer activity tracking
    """
    class Meta:
        model = CustomerActivity
        fields = ['id', 'customer', 'type', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomerWishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for customer wishlist
    """
    class Meta:
        model = CustomerWishlist
        fields = ['id', 'customer', 'book_id', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def validate_book_id(self, value):
        """Validate book_id is positive"""
        if value <= 0:
            raise serializers.ValidationError('Book ID must be positive')
        return value


class CustomerDetailSerializer(serializers.ModelSerializer):
    """
    Detailed customer serializer with related data
    """
    profile = CustomerProfileSerializer(source='customerprofile', read_only=True)
    addresses = CustomerAddressSerializer(source='customeraddress_set', many=True, read_only=True)
    wishlist = CustomerWishlistSerializer(source='customerwishlist_set', many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'name', 'phone', 'address', 'dob', 'gender', 'profile', 'addresses', 'wishlist']
        read_only_fields = ['id']
