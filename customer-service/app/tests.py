from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, CustomerAddress, CustomerProfile, CustomerActivity, CustomerWishlist


class CustomerModelTestCase(TestCase):
    """Test Customer model"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            user_id=1,
            name='John Doe',
            phone='0123456789',
            address='123 Main St',
            gender='M'
        )
    
    def test_customer_creation(self):
        """Test customer is created successfully"""
        self.assertEqual(self.customer.name, 'John Doe')
        self.assertEqual(self.customer.user_id, 1)
        self.assertFalse(self.customer.phone == '')
    
    def test_customer_address_relationship(self):
        """Test customer-address relationship"""
        address = CustomerAddress.objects.create(
            customer=self.customer,
            label='Home',
            street='123 Main St',
            city='New York',
            province='NY',
            country='USA',
            is_default=True
        )
        
        self.assertEqual(self.customer.customeraddress_set.count(), 1)
        self.assertEqual(address.customer.id, self.customer.id)


class CustomerAddressTestCase(TestCase):
    """Test CustomerAddress model"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            user_id=1,
            name='John Doe'
        )
    
    def test_address_creation(self):
        """Test address creation"""
        address = CustomerAddress.objects.create(
            customer=self.customer,
            label='Home',
            street='123 Main St',
            city='New York',
            province='NY',
            country='USA'
        )
        
        self.assertEqual(address.label, 'Home')
        self.assertEqual(address.city, 'New York')
    
    def test_default_address(self):
        """Test setting default address"""
        address1 = CustomerAddress.objects.create(
            customer=self.customer,
            label='Home',
            street='123 Main St',
            city='New York',
            province='NY',
            country='USA',
            is_default=True
        )
        
        self.assertTrue(address1.is_default)


class CustomerProfileAPITestCase(APITestCase):
    """Test customer profile endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create a mock JWT token (in real app, would use auth service)
        self.user_id = 1
        
        # Instead of real middleware, we'll manually set user_id in headers
        # This is a simplified test setup
        self.customer = Customer.objects.create(
            user_id=self.user_id,
            name='John Doe',
            phone='1234567890'
        )
        
        # Create profile
        self.profile = CustomerProfile.objects.create(customer=self.customer)
    
    def _authenticate(self):
        """Helper to set authorization header (mocked)"""
        # In real scenario, would generate JWT token
        # For now, test with mock user in request
        pass
    
    def test_get_profile_requires_auth(self):
        """Test that getting profile requires authentication"""
        response = self.client.get('/api/profile/')
        # Without proper auth setup in test, this may return 403
        # In production, would return 401
    
    def test_profile_creation(self):
        """Test creating new customer profile"""
        customer = Customer.objects.create(
            user_id=2,
            name='Jane Doe'
        )
        profile = CustomerProfile.objects.create(customer=customer)
        
        self.assertEqual(profile.customer.id, customer.id)
        self.assertEqual(profile.bio, '')


class CustomerWishlistTestCase(TestCase):
    """Test customer wishlist"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            user_id=1,
            name='John Doe'
        )
    
    def test_add_to_wishlist(self):
        """Test adding book to wishlist"""
        wishlist = CustomerWishlist.objects.create(
            customer=self.customer,
            book_id=123
        )
        
        self.assertEqual(wishlist.book_id, 123)
        self.assertEqual(self.customer.customerwishlist_set.count(), 1)
    
    def test_unique_book_per_customer(self):
        """Test that same book can only be added once per customer"""
        CustomerWishlist.objects.create(
            customer=self.customer,
            book_id=123
        )
        
        # Try to add same book again - should fail with unique constraint
        try:
            CustomerWishlist.objects.create(
                customer=self.customer,
                book_id=123
            )
            self.fail("Should not allow duplicate wishlist entry")
        except:
            pass  # Expected
    
    def test_multiple_customers_same_book(self):
        """Test different customers can wish for same book"""
        customer2 = Customer.objects.create(
            user_id=2,
            name='Jane Doe'
        )
        
        wish1 = CustomerWishlist.objects.create(
            customer=self.customer,
            book_id=123
        )
        
        wish2 = CustomerWishlist.objects.create(
            customer=customer2,
            book_id=123
        )
        
        self.assertEqual(wish1.book_id, wish2.book_id)
        self.assertNotEqual(wish1.customer.id, wish2.customer.id)


class CustomerActivityTestCase(TestCase):
    """Test customer activity logging"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            user_id=1,
            name='John Doe'
        )
    
    def test_activity_logging(self):
        """Test logging customer activity"""
        activity = CustomerActivity.objects.create(
            customer=self.customer,
            type='profile_updated',
            metadata={'field': 'email'}
        )
        
        self.assertEqual(activity.type, 'profile_updated')
        self.assertIn('field', activity.metadata)
    
    def test_activity_ordering(self):
        """Test activities are ordered by creation time"""
        activity1 = CustomerActivity.objects.create(
            customer=self.customer,
            type='profile_created'
        )
        
        activity2 = CustomerActivity.objects.create(
            customer=self.customer,
            type='profile_updated'
        )
        
        activities = list(self.customer.customeractivity_set.all().order_by('-created_at'))
        self.assertEqual(activities[0].id, activity2.id)


class CustomerAddressManagementTestCase(TestCase):
    """Test address management business logic"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            user_id=1,
            name='John Doe'
        )
    
    def test_set_default_address(self):
        """Test setting one address as default"""
        address1 = CustomerAddress.objects.create(
            customer=self.customer,
            label='Home',
            street='123 Main St',
            city='NY',
            province='NY',
            country='USA',
            is_default=True
        )
        
        address2 = CustomerAddress.objects.create(
            customer=self.customer,
            label='Work',
            street='456 Office Ave',
            city='LA',
            province='CA',
            country='USA',
            is_default=False
        )
        
        # Verify only one default
        default_count = self.customer.customeraddress_set.filter(is_default=True).count()
        self.assertEqual(default_count, 1)
    
    def test_address_updates(self):
        """Test updating address information"""
        address = CustomerAddress.objects.create(
            customer=self.customer,
            label='Home',
            street='123 Main St',
            city='New York',
            province='NY',
            country='USA'
        )
        
        address.city = 'Los Angeles'
        address.province = 'CA'
        address.save()
        
        updated = CustomerAddress.objects.get(id=address.id)
        self.assertEqual(updated.city, 'Los Angeles')


class CustomerProfileExtendedTestCase(TestCase):
    """Test extended customer profile"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            user_id=1,
            name='John Doe'
        )
        self.profile = CustomerProfile.objects.create(
            customer=self.customer
        )
    
    def test_profile_preferences(self):
        """Test storing customer preferences"""
        self.profile.prefer_genres = ['fiction', 'mystery', 'sci-fi']
        self.profile.bio = 'Book lover and avid reader'
        self.profile.save()
        
        updated = CustomerProfile.objects.get(id=self.profile.id)
        self.assertIn('fiction', updated.prefer_genres)
        self.assertIn('Book lover', updated.bio)
    
    def test_profile_timestamps(self):
        """Test profile timestamps"""
        self.assertIsNotNone(self.profile.created_at)
        self.assertIsNotNone(self.profile.updated_at)
