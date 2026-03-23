from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Role, User, UserRole, Token, PasswordReset


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation (handles password)
    """
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        error_messages={
            'min_length': 'Password must be at least 6 characters'
        }
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_email(self, value):
        """Check if email is already registered"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already registered')
        return value
    
    def validate_username(self, value):
        """Check if username is already taken"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username is already taken')
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for user detail (without password)
    """
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'created_at', 'roles']
        read_only_fields = ['id', 'created_at']
    
    def get_roles(self, obj):
        """Get list of roles for this user"""
        roles = Role.objects.filter(userrole__user=obj).values_list('name', flat=True)
        return list(roles)


class UserRoleSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'user', 'token', 'type', 'expires_at', 'revoked']
        read_only_fields = ['id']


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['id', 'user', 'code', 'created_at', 'used_at']
        read_only_fields = ['id', 'created_at', 'used_at']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': 'Old password is required'
        }
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True,
        error_messages={
            'min_length': 'New password must be at least 6 characters',
            'required': 'New password is required'
        }
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True,
        error_messages={
            'min_length': 'Confirmation password must be at least 6 characters',
            'required': 'Password confirmation is required'
        }
    )
    
    def validate(self, attrs):
        """Check if new password matches confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('New passwords do not match')
        return attrs


class AssignRoleSerializer(serializers.Serializer):
    """
    Serializer for assigning roles to users
    """
    user_id = serializers.IntegerField(required=True)
    role_name = serializers.CharField(max_length=100, required=True)
