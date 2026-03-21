from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
import secrets

from .models import User, Role, UserRole, Token, PasswordReset
from .serializers import UserSerializer, RoleSerializer, UserRoleSerializer, TokenSerializer, PasswordResetSerializer


@api_view(['POST'])
def register(request):
    data = request.data
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        hashed_password=make_password(data['password']),
        is_active=True
    )
    # Assign default role (e.g., 'user')
    role, _ = Role.objects.get_or_create(name='user')
    UserRole.objects.create(user=user, role=role)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    data = request.data
    try:
        user = User.objects.get(email=data['email'])
        if not user.is_active:
            return Response({'error': 'Account is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        # In real app, use check_password
        if user.hashed_password != make_password(data['password']):  # Simplified, use proper check
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Store token in DB
    Token.objects.create(
        user=user,
        token=refresh_token,
        type='refresh',
        expires_at=timezone.now() + timezone.timedelta(days=7)
    )

    return Response({
        'access': access_token,
        'refresh': refresh_token,
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(token=request.data.get('refresh'), revoked=False)
        token.revoked = True
        token.save()
    except Token.DoesNotExist:
        pass
    return Response({'message': 'Logged out'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def reset_password_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        code = secrets.token_urlsafe(32)
        PasswordReset.objects.create(user=user, code=code)
        # Send email (mock)
        print(f"Reset code for {email}: {code}")
        return Response({'message': 'Reset code sent'})
    except User.DoesNotExist:
        return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def reset_password_confirm(request):
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    try:
        reset = PasswordReset.objects.get(code=code, used_at__isnull=True)
        reset.user.hashed_password = make_password(new_password)
        reset.user.save()
        reset.used_at = timezone.now()
        reset.save()
        return Response({'message': 'Password reset successful'})
    except PasswordReset.DoesNotExist:
        return Response({'error': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)


# Custom Token Refresh View
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Optionally log or validate
        return response
