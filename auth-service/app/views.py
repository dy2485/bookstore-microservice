from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
import secrets

from .models import User, Role, UserRole, Token, PasswordReset
from .serializers import (
    UserSerializer, RoleSerializer, UserRoleSerializer, 
    TokenSerializer, PasswordResetSerializer, UserDetailSerializer,
    PasswordChangeSerializer, AssignRoleSerializer
)


# ==================== Register & Login ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user
    
    Expected data:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepass123"
    }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Get password from request before saving
        password = request.data.get('password')
        if not password or len(password) < 6:
            return Response(
                {'error': 'Password must be at least 6 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user with hashed password
        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            hashed_password=make_password(password),
            is_active=True
        )
        
        # Assign default role (admin for first user)
        if User.objects.count() == 0:  # First user gets admin role
            role, _ = Role.objects.get_or_create(name='admin')
        else:
            role, _ = Role.objects.get_or_create(name='user')
        UserRole.objects.create(user=user, role=role)
        
        return Response({
            'user': UserDetailSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login user and return JWT tokens
    
    Expected data:
    {
        "email": "john@example.com",
        "password": "securepass123"
    }
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        
        if not user.is_active:
            return Response(
                {'error': 'Account is inactive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check password properly
        if not check_password(password, user.hashed_password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Store refresh token in database
        Token.objects.create(
            user=user,
            token=refresh_token,
            type='refresh',
            expires_at=timezone.now() + timezone.timedelta(days=7)
        )
        
        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user': UserDetailSerializer(user).data
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


# ==================== Token Management ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout user by revoking the refresh token
    
    Expected data:
    {
        "refresh": "refresh_token_value"
    }
    """
    refresh_token = request.data.get('refresh')
    
    if refresh_token:
        try:
            token = Token.objects.get(token=refresh_token, revoked=False)
            token.revoked = True
            token.save()
        except Token.DoesNotExist:
            pass
    
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Verify if the current token is valid and return user info
    """
    try:
        user = request.user
        if user and user.is_active:
            return Response({
                'valid': True,
                'user': UserDetailSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'valid': False, 'error': 'Token user is inactive'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        return Response(
            {'valid': False, 'error': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom JWT token refresh view with validation
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Log token refresh
            pass
        return response


# ==================== Profile Management ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get current user profile with roles
    """
    user = request.user
    roles = Role.objects.filter(userrole__user=user).values_list('name', flat=True)
    
    return Response({
        'user': UserDetailSerializer(user).data,
        'roles': list(roles)
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user profile
    
    Allowed fields:
    - username (cannot change email for security)
    - Only authenticated user can update their own profile
    """
    user = request.user
    
    # Only allow username update
    if 'username' in request.data:
        new_username = request.data['username'].strip()
        if not new_username:
            return Response(
                {'error': 'Username cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if username already exists
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.username = new_username
        user.save()
    
    return Response({
        'message': 'Profile updated successfully',
        'user': UserDetailSerializer(user).data
    }, status=status.HTTP_200_OK)


# ==================== Password Management ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change current user password
    
    Expected data:
    {
        "old_password": "current_password",
        "new_password": "new_secure_password"
    }
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response(
            {'error': 'Both old_password and new_password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify old password
    if not check_password(old_password, user.hashed_password):
        return Response(
            {'error': 'Old password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate new password
    if len(new_password) < 6:
        return Response(
            {'error': 'New password must be at least 6 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update password
    user.hashed_password = make_password(new_password)
    user.save()
    
    return Response({
        'message': 'Password changed successfully'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_request(request):
    """
    Request password reset by sending code to email
    
    Expected data:
    {
        "email": "user@example.com"
    }
    """
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        
        # Generate reset code
        code = secrets.token_urlsafe(32)
        PasswordReset.objects.create(user=user, code=code)
        
        # TODO: In production, send email with reset link
        # send_reset_email(user.email, code)
        
        return Response({
            'message': 'Password reset code sent to email',
            'debug_code': code  # Remove in production!
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        # Don't reveal if email exists
        return Response({
            'message': 'If email exists, reset code was sent'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm(request):
    """
    Confirm password reset with code
    
    Expected data:
    {
        "code": "reset_code_from_email",
        "new_password": "new_secure_password"
    }
    """
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    
    if not code or not new_password:
        return Response(
            {'error': 'Code and new_password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(new_password) < 6:
        return Response(
            {'error': 'Password must be at least 6 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        reset = PasswordReset.objects.get(code=code, used_at__isnull=True)
        
        # Check if code is not expired (valid for 24 hours)
        if timezone.now() - reset.created_at > timezone.timedelta(hours=24):
            return Response(
                {'error': 'Reset code has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update password
        user = reset.user
        user.hashed_password = make_password(new_password)
        user.save()
        
        # Mark code as used
        reset.used_at = timezone.now()
        reset.save()
        
        return Response({
            'message': 'Password reset successful'
        }, status=status.HTTP_200_OK)
        
    except PasswordReset.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired reset code'},
            status=status.HTTP_400_BAD_REQUEST
        )


# ==================== Role Management ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_roles(request):
    """
    List all available roles (admin only)
    """
    if not _is_admin(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_role(request):
    """
    Assign role to user (admin only)
    
    Expected data:
    {
        "user_id": 1,
        "role_name": "admin"
    }
    """
    if not _is_admin(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    role_name = request.data.get('role_name')
    
    if not user_id or not role_name:
        return Response(
            {'error': 'user_id and role_name are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
        role, _ = Role.objects.get_or_create(name=role_name)
        
        # Check if user already has this role
        if UserRole.objects.filter(user=user, role=role).exists():
            return Response(
                {'error': 'User already has this role'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        UserRole.objects.create(user=user, role=role)
        
        return Response({
            'message': f'Role {role_name} assigned to user {user.username}'
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_role(request, user_id, role_name):
    """
    Remove role from user (admin only)
    """
    if not _is_admin(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(name=role_name)
        
        UserRole.objects.filter(user=user, role=role).delete()
        
        return Response({
            'message': f'Role {role_name} removed from user {user.username}'
        }, status=status.HTTP_200_OK)
        
    except (User.DoesNotExist, Role.DoesNotExist):
        return Response(
            {'error': 'User or role not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== Helper Functions ====================

def _is_admin(user):
    """Check if user has admin role"""
    return user.userrole_set.filter(role__name='admin').exists()
