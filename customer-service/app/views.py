from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Customer, CustomerAddress, CustomerProfile, CustomerActivity, CustomerWishlist
from .serializers import (
    CustomerSerializer, CustomerDetailSerializer, CustomerAddressSerializer,
    CustomerProfileSerializer, CustomerActivitySerializer, CustomerWishlistSerializer
)


# ==================== Customer Profile ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_get_profile(request):
    """
    Create or get customer profile for current user
    
    If profile doesn't exist, create it automatically
    """
    user_id = request.user.id
    
    try:
        customer = Customer.objects.get(user_id=user_id)
    except Customer.DoesNotExist:
        # Create new customer profile
        data = request.data
        customer = Customer.objects.create(
            user_id=user_id,
            name=data.get('name', f'User_{user_id}'),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            dob=data.get('dob'),
            gender=data.get('gender', '')
        )
        
        # Create customer profile
        profile = CustomerProfile.objects.create(customer=customer)
        
        # Log activity
        CustomerActivity.objects.create(
            customer=customer,
            type='profile_created'
        )
    
    serializer = CustomerDetailSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Get current user's customer profile
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        serializer = CustomerDetailSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found. Create one first.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user's customer profile
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Log activity
            CustomerActivity.objects.create(
                customer=customer,
                type='profile_updated',
                metadata={'fields': list(request.data.keys())}
            )
            
            return Response(
                {'message': 'Profile updated successfully', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== Customer Addresses ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_addresses(request):
    """
    List all addresses for current user
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        addresses = customer.customeraddress_set.all()
        serializer = CustomerAddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_address(request):
    """
    Create a new address for current user
    
    Expected data:
    {
        "label": "Home",
        "street": "123 Main St",
        "city": "New York",
        "province": "NY",
        "country": "USA",
        "is_default": true
    }
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        
        data = request.data.copy()
        
        # If setting as default, unset all other defaults
        if data.get('is_default'):
            customer.customeraddress_set.filter(is_default=True).update(is_default=False)
        
        serializer = CustomerAddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            
            # Log activity
            CustomerActivity.objects.create(
                customer=customer,
                type='address_added',
                metadata={'label': data.get('label')}
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_address(request, address_id):
    """
    Get specific address details
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        address = customer.customeraddress_set.get(id=address_id)
        serializer = CustomerAddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except CustomerAddress.DoesNotExist:
        return Response(
            {'error': 'Address not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_address(request, address_id):
    """
    Update specific address
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        address = customer.customeraddress_set.get(id=address_id)
        
        data = request.data.copy()
        
        # If setting as default, unset all other defaults
        if data.get('is_default'):
            customer.customeraddress_set.filter(is_default=True).exclude(id=address_id).update(is_default=False)
        
        serializer = CustomerAddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Log activity
            CustomerActivity.objects.create(
                customer=customer,
                type='address_updated',
                metadata={'address_id': address_id}
            )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except (Customer.DoesNotExist, CustomerAddress.DoesNotExist):
        return Response(
            {'error': 'Customer or address not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address(request, address_id):
    """
    Delete specific address
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        address = customer.customeraddress_set.get(id=address_id)
        
        # Cannot delete the last address
        if customer.customeraddress_set.count() == 1:
            return Response(
                {'error': 'Cannot delete the last address'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        address.delete()
        
        # Log activity
        CustomerActivity.objects.create(
            customer=customer,
            type='address_deleted',
            metadata={'address_id': address_id}
        )
        
        return Response(
            {'message': 'Address deleted successfully'},
            status=status.HTTP_200_OK
        )
    
    except (Customer.DoesNotExist, CustomerAddress.DoesNotExist):
        return Response(
            {'error': 'Customer or address not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== Customer Wishlist ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_wishlist(request):
    """
    List all books in customer's wishlist
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        wishlist = customer.customerwishlist_set.all().order_by('-added_at')
        serializer = CustomerWishlistSerializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, book_id):
    """
    Add book to wishlist
    
    URL: /customers/wishlist/{book_id}/
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        
        # Check if already in wishlist
        if customer.customerwishlist_set.filter(book_id=book_id).exists():
            return Response(
                {'error': 'Book already in wishlist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist_item = CustomerWishlist.objects.create(
            customer=customer,
            book_id=book_id
        )
        
        # Log activity
        CustomerActivity.objects.create(
            customer=customer,
            type='book_wishlisted',
            metadata={'book_id': book_id}
        )
        
        serializer = CustomerWishlistSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, book_id):
    """
    Remove book from wishlist
    
    URL: /customers/wishlist/{book_id}/
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        wishlist_item = customer.customerwishlist_set.get(book_id=book_id)
        
        wishlist_item.delete()
        
        # Log activity
        CustomerActivity.objects.create(
            customer=customer,
            type='book_removed_from_wishlist',
            metadata={'book_id': book_id}
        )
        
        return Response(
            {'message': 'Book removed from wishlist'},
            status=status.HTTP_200_OK
        )
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except CustomerWishlist.DoesNotExist:
        return Response(
            {'error': 'Book not in wishlist'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_wishlist(request, book_id):
    """
    Check if book is in customer's wishlist
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        exists = customer.customerwishlist_set.filter(book_id=book_id).exists()
        return Response(
            {'in_wishlist': exists, 'book_id': book_id},
            status=status.HTTP_200_OK
        )
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== Customer Activity ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_activity(request):
    """
    List customer activity history
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        
        # Get activity, paginated
        activity_type = request.query_params.get('type')
        queryset = customer.customeractivity_set.all().order_by('-created_at')
        
        if activity_type:
            queryset = queryset.filter(type=activity_type)
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_qs = paginator.paginate_queryset(queryset, request)
        
        serializer = CustomerActivitySerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_activity(request):
    """
    Log custom activity for customer
    
    Expected data:
    {
        "type": "book_viewed",
        "metadata": {"book_id": 123}
    }
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        
        activity_type = request.data.get('type')
        metadata = request.data.get('metadata', {})
        
        if not activity_type:
            return Response(
                {'error': 'Activity type is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        activity = CustomerActivity.objects.create(
            customer=customer,
            type=activity_type,
            metadata=metadata
        )
        
        serializer = CustomerActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== Customer Profile Extended ====================

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def manage_customer_profile(request):
    """
    Manage extended customer profile (bio, preferences)
    
    GET: Get profile
    POST/PUT/PATCH: Update profile
    """
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        
        if request.method == 'GET':
            try:
                profile = customer.customerprofile
                serializer = CustomerProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomerProfile.DoesNotExist:
                # Create profile if doesn't exist
                profile = CustomerProfile.objects.create(customer=customer)
                serializer = CustomerProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:  # POST, PUT, PATCH
            try:
                profile = customer.customerprofile
            except CustomerProfile.DoesNotExist:
                profile = CustomerProfile.objects.create(customer=customer)
            
            serializer = CustomerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
