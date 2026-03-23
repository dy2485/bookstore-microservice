from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Role, UserRole, Token, PasswordReset
import json


class UserModelTestCase(TestCase):
    """Test User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            hashed_password=make_password('password123'),
            is_active=True
        )
    
    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_active)
        self.assertTrue(check_password('password123', self.user.hashed_password))
    
    def test_user_string_representation(self):
        """Test user __str__ method"""
        self.assertEqual(str(self.user), 'testuser')


class RoleModelTestCase(TestCase):
    """Test Role model"""
    
    def setUp(self):
        self.role = Role.objects.create(
            name='admin',
            permissions={'create': True, 'delete': True}
        )
    
    def test_role_creation(self):
        """Test role is created successfully"""
        self.assertEqual(self.role.name, 'admin')
        self.assertIn('create', self.role.permissions)


class AuthenticationAPITestCase(APITestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            hashed_password=make_password('password123'),
            is_active=True
        )
        role, _ = Role.objects.get_or_create(name='user')
        UserRole.objects.create(user=self.user, role=role)
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    def test_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        url = reverse('register')
        data = {
            'username': 'anotheruser',
            'email': 'test@example.com',  # Same as existing user
            'password': 'securepass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', str(response.data))
    
    def test_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        url = reverse('register')
        data = {
            'username': 'testuser',  # Same as existing user
            'email': 'different@example.com',
            'password': 'securepass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_short_password(self):
        """Test registration with short password"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123'  # Too short
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_success(self):
        """Test successful login"""
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_login_wrong_password(self):
        """Test login with wrong password"""
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent email"""
        url = reverse('login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_inactive_user(self):
        """Test login with inactive user"""
        # Create inactive user
        User.objects.create(
            username='inactiveuser',
            email='inactive@example.com',
            hashed_password=make_password('password123'),
            is_active=False
        )
        
        url = reverse('login')
        data = {
            'email': 'inactive@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenAPITestCase(APITestCase):
    """Test token-related endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            hashed_password=make_password('password123'),
            is_active=True
        )
        
        # Login to get tokens
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'password123'
        }, format='json')
        
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
    
    def test_verify_token_valid(self):
        """Test verifying valid token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse('verify_token'), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_verify_token_invalid(self):
        """Test verifying invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(reverse('verify_token'), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileAPITestCase(APITestCase):
    """Test profile endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            hashed_password=make_password('password123'),
            is_active=True
        )
        role, _ = Role.objects.get_or_create(name='user')
        UserRole.objects.create(user=self.user, role=role)
        
        # Login
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'password123'
        }, format='json')
        
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_get_profile(self):
        """Test getting user profile"""
        response = self.client.get(reverse('profile'), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertIn('user', response.data)
        self.assertIn('roles', response.data)
    
    def test_update_profile(self):
        """Test updating user profile"""
        url = reverse('update_profile')
        data = {'username': 'newusername'}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'newusername')
        
        # Verify in database
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, 'newusername')
    
    def test_update_profile_duplicate_username(self):
        """Test updating profile with duplicate username"""
        # Create another user
        User.objects.create(
            username='otheruser',
            email='other@example.com',
            hashed_password=make_password('password123')
        )
        
        url = reverse('update_profile')
        data = {'username': 'otheruser'}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordAPITestCase(APITestCase):
    """Test password management endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            hashed_password=make_password('password123'),
            is_active=True
        )
        
        # Login
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'password123'
        }, format='json')
        
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_change_password_success(self):
        """Test successful password change"""
        url = reverse('change_password')
        data = {
            'old_password': 'password123',
            'new_password': 'newpassword456'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify new password works
        self.user.refresh_from_db()
        self.assertTrue(check_password('newpassword456', self.user.hashed_password))
    
    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password"""
        url = reverse('change_password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword456'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_reset_password_request(self):
        """Test password reset request"""
        url = reverse('reset_password_request')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PasswordReset.objects.filter(user=self.user).exists())
    
    def test_reset_password_confirm_success(self):
        """Test password reset confirmation"""
        # Create reset request
        reset = PasswordReset.objects.create(
            user=self.user,
            code='test_code_12345'
        )
        
        url = reverse('reset_password_confirm')
        data = {
            'code': 'test_code_12345',
            'new_password': 'resetpassword789'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password changed
        self.user.refresh_from_db()
        self.assertTrue(check_password('resetpassword789', self.user.hashed_password))
    
    def test_reset_password_invalid_code(self):
        """Test password reset with invalid code"""
        url = reverse('reset_password_confirm')
        data = {
            'code': 'invalid_code',
            'new_password': 'resetpassword789'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutAPITestCase(APITestCase):
    """Test logout endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            hashed_password=make_password('password123'),
            is_active=True
        )
        
        # Login
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'password123'
        }, format='json')
        
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_logout_success(self):
        """Test successful logout"""
        url = reverse('logout')
        data = {'refresh': self.refresh_token}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
